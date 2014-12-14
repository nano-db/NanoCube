class QueryBuilder(object):
    def __init__(self, cube):
        super(QueryBuilder, self).__init__()
        self.cube = cube
        self.path = []

    def where(self, **kwargs):
        
        return self

    def _retrieve_timeserietable(self, path):
        node = self.cube.world

        remaining_levels = self.cube.dimension
        for level_path in path:
            for key in level_path:
                node = node.get_child(key)
                if node is None:
                    return node
            remaining_levels -= 1
            node = node.content

        for i in range(remaining_levels):
            node = node.content

        return node

    def count(self):
        table = self._retrieve_timeserietable(self.path)
        if table is None:
            return 0
        else:
            return table.query()