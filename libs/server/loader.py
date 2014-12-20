import yaml
import csv
import logging
from threading import Thread
from datetime import datetime
from libs.server.nanocube import NanoCube


def create_nanocube(config_path):
    stream = file(config_path, 'r')
    config = yaml.load(stream)

    name = config['Name']
    dimensions_name = map(lambda d: d['Name'], config['Dimensions'])

    cube = NanoCube(
        dimensions_name,
        name=name,
        loc_granularity=config['Location granularity'],
        bin_size=config['Meta']['Time bin size']
    )

    parsing_method = _generate_parsing_method(config)
    return cube, parsing_method


def load_data_in_cube(cube, parsing_func, data_path):
    t = Thread(target=parsing_func, args=(cube, data_path))
    t.daemon = True
    t.start()


def _generate_parsing_method(config):
    long_key = config['Meta']['Longitude key']
    lat_key = config['Meta']['Latitude key']
    time_key = config['Meta']['Time key']
    time_format = config['Meta']['Time format']
    limit = config.get('Limit')

    def parsing(cube, input_file):
        logger = logging.getLogger("nanoDB.loader." + cube.name)

        data_file = open(input_file, 'r')
        reader = csv.DictReader(data_file, delimiter=",")
        cube.is_loading = True
        for row in reader:
            if limit is not None and cube.count > limit:
                break

            event = dict()
            try:
                event['Longitude'] = float(row[long_key])
                event['Latitude'] = float(row[lat_key])
                event['Time'] = datetime.strptime(row[time_key], time_format)
                for dim in config['Dimensions']:
                    event[dim['Name']] = row[dim['Key']]
                cube.add(event)
            except Exception, e:
                logger.debug(e)

        cube.is_loading = False
    return parsing