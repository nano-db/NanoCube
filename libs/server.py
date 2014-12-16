import argparse
import zmq


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
            self.loop()
        except KeyboardInterrupt:
            print('Bye')

    def loop(self):
        msg = self.socket.recv()
        self.socket.send(msg)

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