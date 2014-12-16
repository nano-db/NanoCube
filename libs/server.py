import argparse

class ServerManager(object):
    def __init__(self, args):
        super(ServerManager, self).__init__()
        self.debug = args.debug
        self.port = args.port
        self.cubes = dict()

    def start(self):
        self.loop()

    def loop(self):
        try:
            bob = 0
            while True:
                bob += 1
        except KeyboardInterrupt:
            print('Bye')

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