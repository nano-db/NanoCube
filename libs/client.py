import argparse
import zmq
from cmd import Cmd


class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)



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
        print('\nBye')

if __name__ == '__main__':
    init_parser()