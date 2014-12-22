import os
from cmd import Cmd
from nanodb_driver.driver import Driver


class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)
        self.connector = Driver(port=args.port)
        self.cache = None

        if not self.connector.is_connected:
            print("Impossible to connect to server on port: {0}".format(args.port))
            exit(1)
        else:
            self._update_cache()

    def _update_cache(self):
        self.cache = self.connector.list_cubes()

    def _cube_start_with(self, text):
        res = []
        for cube in self.cache:
            name = cube['name']
            if len(text) == 0 or name.startswith(text):
                res.append(cube['name'])
        return res

    def do_list(self, _):
        """list
        List all the cubes already loaded in nanodb"""
        cubes = self.connector.list_cubes()
        self.cache = cubes
        pattern = '- {0}      Size: {1}      Loading: {2}'
        for cube in cubes:
            print(pattern.format(cube['name'], cube['count'], cube['is_loading']))

    def do_info(self, args):
        """info <cube name>
        Return cube information"""
        name = args.strip()
        try:
            info = self.connector.get_information(name)
        except Exception, e:
            print('[Error] ' + str(e))
        else:
            for key in info:
                print(key + ": " + str(info[key]))

    def complete_info(self, text, line, start_index, end_index):
        return self._cube_start_with(text)

    def do_load(self, args):
        """load <csv file> <yml file> | load <nano file>
        Load in server a cube. The command can receive as attribute a .csv
        file and a configuration file or an already serialized cube stored
        in a .nano file"""
        args = args.strip().split(" ")
        if len(args) > 2 or len(args) == 0:
            print('[Error] An input file and a configuration file are needed')
            return

        paths = []
        for f in args:
            if not os.path.isfile(f):
                print("Impossible to locate: {0}".format(f))
                return
            paths.append(os.path.abspath(f))

        try:
            if len(paths) == 1:
                self.connector.load_cube(paths[0])
            else:
                ret = self.connector.create_cube(paths[0], paths[1])
                print("Loading: {0}".format(ret["name"]))
        except Exception, e:
            print('[Error] ' + str(e))

    def do_serialize(self, args):
        """serialize <cube name> <path>
        Serialize a cube in a .nano file. The path parameter specify where
        the cube will be store."""
        args = args.strip().split(" ")
        if len(args) < 1:
            print('[Error] A cube name should at least be specified.')

        try:
            if len(args) == 2:
                ret = self.connector.serialize(args[0], args[1])
            else:
                ret = self.connector.serialize(args[0])

            path = ret.get('file')
            print(path)
        except Exception, e:
            print('[Error] ' + str(e))

    def complete_serialize(self, text, line, start_index, end_index):
        return self._cube_start_with(text)

    def do_drop(self, args):
        """drop <cube name>
        Delete an existing cube in th server"""
        try:
            self.connector.drop(args)
        except Exception, e:
            print('[Error] ' + str(e))

    def complete_drop(self, text, line, start_index, end_index):
        return self._cube_start_with(text)

    def do_exit(self, _):
        print("Au revoir!")
        exit(0)