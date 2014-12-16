import argparse
import zmq
import json


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
        cmd = msg['cmd']
        if cmd == "ping":
            return self.ping()
        elif cmd == "list":
            return self.list()
        else:
            return self.not_found()

    def ping(self):
        return {
            "status": "OK"
        }

    def list(self):
        return {
            "status": "OK",
            "data": self.cubes.keys()
        }

    def not_found(self):
        return {
            "status": "error",
            "error": "Command not found"
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