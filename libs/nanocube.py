from libs.node import Node
from libs.timeserietable import TimeSerieTable


class NanoCube(object):
    def __init__(self, dimensions, locGranularity=10):
        super(NanoCube, self).__init__()
        self.world = Node()
        self.location_granularity = locGranularity

        # Init dimensions
        self.dimensions = dimensions
        self.dim_mapping = dict()
        for dim in dimensions:
            self.dim_mapping[dim] = dict()

    def add(self, entry):
        updated_nodes = []
        self._add_node(self.world, entry, 1, updated_nodes)

    def get_dimension(self):
        return len(self.dimensions) + 2

    def _add_node(self, root, entry, level, updated_nodes):
        child = None
        keys = self._keys_at_level(entry, level)
        stack = self._trail_proper_path(root, keys)
        while len(stack) > 0:
            n = stack.pop()
            update = False

            if n.has_a_single_child():
                n.set_shared_content(child)
            elif n.content is None:
                dim = self.get_dimension()
                if level == dim:
                    n.set_proper_content(TimeSerieTable())
                else:
                    n.set_proper_content(Node())
                update = True
            elif n.has_shared_content() and n.content not in updated_nodes:
                raise Exception("Not implemented")
                update = True
            elif n.has_proper_content():
                update = True

            if update:
                if level == self.get_dimension():
                    n.content.insert(entry['Time'])
                else:
                    self._add_node(n.content, entry, level + 1, updated_nodes)
                updated_nodes.append(n.content)
            child = n

    def _trail_proper_path(self, root, keys):
        stack = []
        n = root
        stack.append(root)
        for key in keys:
            child = n.get_child(key)
            if child is None:
                child = Node()
                n.add_proper_child(key, child)
            elif Node.is_shared_child(n, child):
                raise Exception("Not implemented")
            stack.append(child)
            n = child
        return stack

    def _keys_at_level(self, entry, level):
        if level == 1:
            return self._get_location_keys(entry, self.location_granularity)
        else:
            return self._get_category_keys(entry, level)

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

    def _get_category_keys(self, entry, level):
        selected_level = level - 2
        dim_name = self.dimensions[selected_level]
        mapping = self.dim_mapping[dim_name]

        if mapping.get(entry.get(dim_name)) is None:
            new_key = str(len(mapping))
            mapping[entry.get(dim_name)] = new_key
            return [new_key]
        else:
            return [mapping.get(entry.get(dim_name))]


    def _shallow_copy(node):
        copied_node = Node()
        copied_node.set_shared_content(node.content)
        return copied_node
