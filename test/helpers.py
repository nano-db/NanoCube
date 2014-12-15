import csv
import datetime
import os
from libs.nanocube import NanoCube

samples = dict(
    simple=dict(
        path=os.path.dirname(__file__) + "/samples/simple_cube.csv",
        schema=["Devise"],
        loc_granularity=2
    )
)


def mock_cube(name="simple"):
    parser = '%m/%d/%Y %H:%M:%S'
    cube = NanoCube(samples[name]['schema'], loc_granularity=samples[name]['loc_granularity'])

    with open(samples[name]['path']) as sample_file:
        reader = csv.DictReader(sample_file, delimiter=",")
        for row in reader:
            data = dict()
            data['Longitude'] = float(row['Longitude'])
            data['Latitude'] = float(row['Latitude'])
            data['Time'] = datetime.datetime.strptime(row['Time'], parser)
            data['Devise'] = row['Devise']
            cube.add(data)
    return cube
