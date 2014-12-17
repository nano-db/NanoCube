import argparse
import zmq
import yaml
import datetime
import csv
import ujson
from threading import Thread
from nanocube import NanoCube


class ServerManager(object):
    def __init__(self, args):
        super(ServerManager, self).__init__()
        self.debug = args.debug
        self.port = args.port
        self.cubes = dict()

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:{0}".format(args.port))

    def start(self):
        print("NanocubeDB is running on port: {0}".format(self.port))
        try:
            while True:
                self.loop()
        except KeyboardInterrupt:
            print('Bye')

    def loop(self):
        msg = self.socket.recv_json()
        ret = self.route(msg)
        self.socket.send_json(ret)

    def route(self, msg):
        cmd = msg.get('cmd')
        data = msg.get('data')
        print("Command: {0}, Data: {1}".format(cmd, data))

        if cmd == "ping":
            return self.ping()
        elif cmd == "list":
            return self.list()
        elif cmd == "info":
            return self.info(data)
        elif cmd == "load":
            return self.load(data)
        elif cmd == "serialize":
            return self.serialize(data)
        else:
            return self.not_found()

    def ping(self):
        return {
            "status": "OK"
        }

    def list(self):
        return {
            "status": "OK",
            "data": [self.cubes[name].info for name in self.cubes]
        }

    def not_found(self):
        return {
            "status": "error",
            "error": "Command not found"
        }

    def info(self, data):
        cube_name = data["cube"]
        if self.cubes.get(cube_name) is None:
            return {
                "status": "error",
                "error": "Cube {0} not found".format(cube_name)
            }
        else:
            return {
                "status": "OK",
                "data": self.cubes[cube_name].info
            }

    def create_nanocube(self, config):
        name = config['Name']
        dimensions_name = map(lambda d: d['Name'], config['Dimensions'])

        if self.cubes.get(name) is not None:
            raise Exception("Name {0} is already used".format(name))

        cube = NanoCube(
            dimensions_name,
            name=name,
            loc_granularity=config['Location granularity'],
            bin_size=config['Meta']['Time bin size']
        )
        self.cubes[name] = cube

        return cube

    def parsing_method(self, config):
        long_key = config['Meta']['Longitude key']
        lat_key = config['Meta']['Latitude key']
        time_key = config['Meta']['Time key']
        time_format = config['Meta']['Time format']

        def parsing(cube, input_file):
            data_file = open(input_file, 'r')
            reader = csv.DictReader(data_file, delimiter=",")
            cube.is_loading = True
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

            cube.is_loading = False
        return parsing

    def load(self, data):
        config_path = data.get('config')
        input_path = data.get('input')

        try:
            stream = file(config_path, 'r')
            config = yaml.load(stream)
            cube = self.create_nanocube(config)
        except Exception, e:
            return {
                "status": "error",
                "error": str(e)
            }

        parsing = self.parsing_method(config)
        t = Thread(target=parsing, args=(cube, input_path))
        t.daemon = True
        info = cube.info
        t.start()

        return {
            "status": "OK",
            "data": info
        }

    def serialize(self, data):
        cube_name = data.get('cube')
        if self.cubes.get(cube_name) is None:
            return {
                "status": "error",
                "error": "Cube {0} not found".format(cube_name)
            }
        else:
            self.cubes.get(cube_name)
            return {
                "status": "OK",
                "data": "done"
            }


def init_parser():
    parser = argparse.ArgumentParser(description="NanocubeBD: Real-time database")
    parser.add_argument('--debug', '-d', action='store_true',
                        help="Start in Debug mode")
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help="Interface port")
    args = parser.parse_args()
    s = ServerManager(args)
    s.start()

if __name__ == '__main__':
    init_parser()