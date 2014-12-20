import argparse
import logging
from libs.server.interface import Interface


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