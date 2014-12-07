from libs.node import Node


class NanoCube(object):
    def __init__(self, dimensions, locGranularity=10):
        super(NanoCube, self).__init__()
        self.world = Node()
        self.location_granularity = locGranularity

        # Init dimensions
        self.dim_mapping = dict()
        for dim in dimensions:
            self.dim_mapping[dim] = dict()

    def add(self, entry):
        updated_nodes = []
        self._add_node(entry, 1, updated_nodes)

    def _add_node(self, entry, level, updated_nodes):
        child = None
        keys = self._keys_at_level(entry, level)
        stack = self._trail_proper_path(keys)
        while len(stack) > 0:
            n = stack.pop()
            update = False
            if n.has_a_single_child():
                n.set_shared_content(child)

    def _trail_proper_path(self, keys):
        stack = []
        stack.append(self.root)
        n = self.root
        for key in keys:
            child = n.get_child(key)
            if child is None:
                child = Node()
                n.add_proper_child(child)
            elif Node.is_shared_child(n, child):
                # To handle
                pass
            stack.append(child)
            n = child
        return stack

    def _keys_at_level(self, entry, level):
        maxLevel = len(self.dimensions) + self.location_granularity + 1
        if level < 1 or level > maxLevel:
            raise AttributeError

        ret = []
        if level <= self.location_granularity:
            ret = self._get_location_keys(entry, level)
        else:
            ret = self._get_location_keys(entry, self.location_granularity)

        return ret

    def _get_location_keys(self, entry, level):
        keys = []
        lat_bounds = {
            'max': 85,
            'min': -85
        }
        long_bounds = {
            'max': 180,
            'min': -180
        }

        for i in range(level):
            prev = "," if i == 0 else keys[i - 1]
            prev_long = prev.split(",")[0]
            prev_lat = prev.split(",")[1]

            lat_mean = (lat_bounds['max'] + lat_bounds['min']) / 2
            if entry['Latitude'] > lat_mean:
                lat_bounds['min'] = lat_mean
                prev_lat += "1"
            else:
                lat_bounds['max'] = lat_mean
                prev_lat += "0"

            long_mean = (long_bounds['max'] + long_bounds['min']) / 2
            if entry['Longitude'] > long_mean:
                long_bounds['min'] = long_mean
                prev_long += "1"
            else:
                long_bounds['max'] = long_mean
                prev_long += "0"

            keys.append(prev_long + "," + prev_lat)

        return keys

    def _get_category_key(self, entry, level):
        pass
