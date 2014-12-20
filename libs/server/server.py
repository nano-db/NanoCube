import argparse
import logging
from libs.server.serializer import dump
from libs.server.loader import create_nanocube, load_data_in_cube, load_from_nano_file
from libs.server.interface import Interface


def init_parser():
    parser = argparse.ArgumentParser(description="NanocubeBD: Real-time database")
    parser.add_argument('--debug', '-d', action='store_true',
                        help="Start in Debug mode")
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help="Interface port")
    args = parser.parse_args()
    s = ServerManager(args)
    s.start()


class ServerManager(Interface):
    def __init__(self, args):
        super(ServerManager, self).__init__(args.port)
        self.debug = args.debug
        self.cubes = dict()

        self.logger = logging.getLogger("nanoDB")
        fh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def start(self):
        self.logger.info("NanoDB starting on port: {}".format(self.port))
        super(ServerManager, self).start()

    def _precmd(self, cmd, msg):
        self.logger.info(str(cmd) + " - " + str(msg))

    def do_ping(self, _):
        return self._send_success("pong")

    def do_list(self, _):
        cubes = [self.cubes[name].info for name in self.cubes]
        return self._send_success(cubes)

    def do_info(self, data):
        cube_name = data.get('cube')
        if self.cubes.get(cube_name) is None:
            error = "Cube '{}' not found".format(cube_name)
            return self._send_error(error)
        else:
            return self._send_success(self.cubes[cube_name].info)

    def do_create(self, data):
        config_path = data.get('config')
        input_path = data.get('input')

        try:
            cube, parsing_method = create_nanocube(config_path)
            if self.cubes.get(cube.name) is not None:
                raise Exception("Cube already exists")
            else:
                self.cubes[cube.name] = cube
            load_data_in_cube(cube, parsing_method, input_path)
        except Exception, e:
            return self._send_error(e)
        else:
            return self._send_success(cube.info)

    def do_load(self, data):
        nano_path = data.get('file')
        try:
            cube_name = load_from_nano_file(nano_path, self.cubes)
            return self._send_success({"cube": cube_name})
        except Exception, e:
            self.logger.error(e)
            return self._send_error(e)

    def do_serialize(self, data):
        cube_name = data.get('cube')
        if self.cubes.get(cube_name) is None:
            error = "Cube '{}' not found".format(cube_name)
            return self._send_error(error)
        else:
            cube = self.cubes.get(cube_name)
            file_name = "data/{}.nano".format(cube.name)
            dump(cube, file_name)
            return self._send_success({
                'file': file_name
            })

    def do_drop(self, data):
        cube_name = data.get('cube')
        if self.cubes.get(cube_name) is None:
            error = "Cube '{}' not found".format(cube_name)
            return self._send_error(error)
        else:
            del self.cubes[cube_name]
            return self._send_success("Dropped")

if __name__ == '__main__':
    init_parser()