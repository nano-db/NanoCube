from cmd import Cmd
from connector import Connector

class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)
        connector = Connector(args.port)

        if not connector.is_connected:
            print("Impossible to connect to server on port: {0}".format(args.port))
            exit(1)

    def do_exit(self, args):
        print("Bye!")
        exit(0)