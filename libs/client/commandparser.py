import os
from cmd import Cmd

from libs.shared.connector import Connector


class CommandParser(Cmd):
    def __init__(self, args):
        Cmd.__init__(self)
        self.connector = Connector(args.port)
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
        cubes = self.connector.list_cubes()
        self.cache = cubes
        pattern = '- {0}      Size: {1}      Loading: {2}'
        for cube in cubes:
            print(pattern.format(cube['name'], cube['count'], cube['is_loading']))

    def do_info(self, args):
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
            ret = self.connector.load_cube(paths[0], paths[1])
        except Exception, e:
            print('[Error] ' + str(e))
        else:
            print("Loading: {0}".format(ret["name"]))

    def do_serialize(self, args):
        try:
            self.connector.serialize(args)
        except Exception, e:
            print('[Error] ' + str(e))


    def complete_serialize(self, text, line, start_index, end_index):
        return self._cube_start_with(text)

    def do_exit(self, _):
        print("Au revoir!")
        exit(0)