import argparse
import zmq
from cmd import Cmd


class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:{0}".format(args.port))
        self.socket = socket

    def do_ping(self, args):
        print("ping")
        try:
            self.socket.send(args)
            res = self.socket.recv()
            print(res)
        except zmq.error.ZMQError:
            print("Impossible to connect")

    def do_exit(self, args):
        print("Bye!")
        exit(0)


def init_parser():
    parser = argparse.ArgumentParser(description="NanocubeBD client")
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help="Interface port")
    args = parser.parse_args()
    prompt = CommandParser(args)
    prompt.prompt = '> '
    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        prompt.do_exit(None)

if __name__ == '__main__':
    init_parser()