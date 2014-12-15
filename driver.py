import csv
import datetime
import sys
from libs.nanocube import NanoCube


def main():
    parser = '%m/%d/%Y %I:%M:%S %p'
    cube = NanoCube(['Description'], 2)
    with open('data/crime50k.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = dict()
            data['Longitude'] = float(row['Longitude'])
            data['Latitude'] = float(row['Latitude'])
            data['Time'] = datetime.datetime.strptime(row['time'], parser)
            data['Description'] = row['crime']
            cube.add(data)
    print(sys.getsizeof(cube))


if __name__ == '__main__':
    main()
