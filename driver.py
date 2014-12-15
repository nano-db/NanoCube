import csv
import datetime
import argparse
import yaml
from libs.nanocube import NanoCube


def create_nanocube(kwargs):
    config  = yaml.load(kwargs.config)
    dimensions_name = map(lambda d: d['Name'], config['Dimensions'])

    cube = NanoCube(
        config['Name'],
        dimensions_name,
        loc_granularity=config['Location granularity'],
        bin_size=config['Meta']['Time bin size']
    )

    long_key = config['Meta']['Longitude key']
    lat_key = config['Meta']['Latitude key']
    time_key = config['Meta']['Time key']
    time_format = config['Meta']['Time format']

    reader = csv.DictReader(kwargs.input, delimiter=",")
    for row in reader:
        event = dict()
        try:
            event['Longitude'] = float(row[long_key])
            event['Latitude'] = float(row[lat_key])
            event['Time'] = datetime.datetime.strptime(row[time_key], time_format)
            for dim in config['Dimensions']:
                event[dim['Name']] = row[dim['Key']]
            cube.add(event)
        except Exception:
            pass



def init_parser():
    parser = argparse.ArgumentParser(description="Nanocube real-time database")
    parser.add_argument('input', type=file,
                        help="File containing the data to insert in the Nanocube")
    parser.add_argument('config', type=file,
                        help="Configuration file to parse the input file")
    args = parser.parse_args()

    create_nanocube(args)

if __name__ == '__main__':
    init_parser()
