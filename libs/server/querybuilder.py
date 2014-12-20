class QueryBuilder(object):
    def __init__(self, cube, **kwargs):
        super(QueryBuilder, self).__init__()
        self.cube = cube
        self.path = [[] for _ in range(cube.get_dimension())]
        self.precision = [0 for _ in range(cube.get_dimension())]
        self.timeframe = [None, None]

        if kwargs.has_key('debug'):
            self._init_debug()
        else:
            self.debug = False

    def find(self, dimension_name, dive):
        if dimension_name not in self.cube.dimensions and dimension_name != "Location":
            raise Exception("Dimension '{0}' not found.".format(dimension_name))

        if dimension_name == "Location":
            path_index = 0
        else:
            path_index = self.cube.dimensions.index(dimension_name) + 1

        if len(self.path[path_index]) != 0:
            raise Exception("Try to override dimension: {0}".format(dimension_name))

        if isinstance(dive, tuple):
            new_path = dive[0]
            new_precision = dive[1]
        else:
            new_path = [dive]
            new_precision = 0

        self.path[path_index] = new_path
        self.precision[path_index] = new_precision
        return self

    def after(self, date):
        self.timeframe[0] = date
        return self

    def before(self, date):
        self.timeframe[1] = date
        return self

    def between(self, begin, end):
        self.after(begin)
        self.before(end)
        return self

    def _retrieve_timeserietable(self, path):
        node = self.cube.world

        remaining_levels = self.cube.get_dimension()
        for level_path in path:
            if self.debug:
                visited_links = []

            for key in level_path:
                if node.has_shared_content:
                    break
                node = node.get_child(key)
                if node is None:
                    return node
                elif self.debug:
                    visited_links.append(key)

            remaining_levels -= 1
            node = node.content
            if self.debug:
                self.trace.append(visited_links)

        for i in range(remaining_levels):
            node = node.content
            if self.debug:
                self.trace.append([])

        return node

    def execute(self, **kwargs):
        if kwargs.has_key('debug'):
            self._init_debug()

        table = self._retrieve_timeserietable(self.path)
        if table is None:
            return 0
        else:
            return table.query(self.timeframe[0], self.timeframe[1])

    def _init_debug(self):
        self.debug = True
        self.trace = []