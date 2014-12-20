import argparse
from libs.server.interface import Interface


class ServerManager(Interface):
    def __init__(self, args):
        super(ServerManager, self).__init__(args.port)
        self.debug = args.debug
        self.cubes = dict()

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