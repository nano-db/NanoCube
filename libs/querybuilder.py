class QueryBuilder(object):
    def __init__(self, cube, **kwargs):
        super(QueryBuilder, self).__init__()
        self.cube = cube
        self.path = [[] for _ in range(cube.get_dimension())]
        self.precision = [0 for _ in range(cube.get_dimension())]
        self.timeframe = [None, None]

    def find(self, dimension_name, dive):
        if dimension_name not in self.cube.dimension and dimension_name != "Location":
            raise Exception("Dimension '{0}' not found.".format(dimension_name))

        if dimension_name == "Location":
            path_index = 0
        else:
            path_index = self.cube.dimension.index(dimension_name) + 1

        if len(self.path[path_index]) != 0:
            raise Exception("Try to override dimension: {0}".format(dimension_name))

        if isinstance(dive, tuple):
            new_path = dive[0]
            new_precision = dive[1]
        else:
            new_path = dive
            new_precision = 0

        self.path[path_index] = new_path
        self.precision[path_index] = new_precision
        return self

    def after(self, date):
        self.timeframe[0] = date

    def before(self, date):
        self.timeframe[1] = date

    def between(self, begin, end):
        self.after(begin)
        self.before(end)

    def _retrieve_timeserietable(self, path):
        node = self.cube.world

        remaining_levels = self.cube.get_dimension()
        for level_path in path:
            for key in level_path:
                if node.has_shared_content:
                    break
                node = node.get_child(key)
                if node is None:
                    return node
            remaining_levels -= 1
            node = node.content

        for i in range(remaining_levels):
            node = node.content

        return node

    def execute(self):
        table = self._retrieve_timeserietable(self.path)
        if table is None:
            return 0
        else:
            return table.query(self.timeframe[0], self.timeframe[1])