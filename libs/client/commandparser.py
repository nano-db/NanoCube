import os
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
            print('[Error] A name should be specified')
        else:
            try:
                self.connector.use_cube(cube_name)
            except Exception, e:
                print('[Error] ' + e)

    def do_load(self, args):
        args = args.strip().split(" ")
        if len(args) != 2:
            print('[Error] An input file and a configuration file are needed')
            return

        paths = []
        for f in args:
            if not os.path.isfile(f):
                print("Impossible to locate: {0}".format(f))
                return
            paths.append(os.path.abspath(f))

        try:
            ret = self.connector.load(paths[0], paths[1])
        except Exception, e:
            print('[Error] ' + e)
        else:
            print("Loading: {0}".format(ret["name"]))

    def do_exit(self, args):
        print("Bye!")
        exit(0)