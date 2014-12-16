from cmd import Cmd
from connector import Connector

class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)
        self.connector = Connector(args.port)

        if not self.connector.is_connected:
            print("Impossible to connect to server on port: {0}".format(args.port))
            exit(1)

    def do_list(self, args):
        cubes = self.connector.list_cubes()
        print('{0} cubes'.format(len(cubes)))
        for cube in cubes:
            print('- {0}'.format(cube))

    def do_use(self, cube_name):
        if not cube_name:
            print('A name should be specified')
        else:
            self.connector.use_cube(cube_name)

    def do_exit(self, args):
        print("Bye!")
        exit(0)