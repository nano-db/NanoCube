import io
import re
from nanocube import NanoCube
from node import Node
from timeserietable import TimeSerieTable


def dumps(cube):
    '''Serialize a cube and return the string'''
    stream = io.StringIO()
    _dumper(cube, stream)
    res = stream.getvalue()
    stream.close()
    return res


def dump(cube, file_name):
    '''Serialize a cube and write it to the passed file'''
    stream = io.open(file_name, mode="w")
    _dumper(cube, stream)
    stream.close()


def _dumper(cube, stream):
    _dump_cube(cube, stream)
    _dump_nodes(cube.world, stream)


def loads(string):
    '''Unserialize a cube from the passed string and return it'''
    stream = io.StringIO(string)
    cube = _loader(stream)
    stream.close()
    return cube


def load(file_name):
    '''Unserialize a cube stored in a file and return it'''
    stream = io.open(file_name)
    cube = _loader(stream)
    stream.close()
    return cube


def _loader(stream):
    cube = _load_cube(stream)
    cube.world = _load_nodes(stream)
    return cube


def _load_cube(stream):
    name = None
    dim = None
    count = 0
    gran = 0
    dim_mapping = {}

    for i in range(5):
        line = stream.readline().encode('utf-8')
        if i == 0:
            name = re.search("name: '(.+)'\n", line).group(1)
        elif i == 1:
            count = re.search("count: (\d+)\n", line).group(1)
            count = int(count)
        elif i == 2:
            gran = re.search("gran: (\d+)\n", line).group(1)
            gran = int(gran)
        elif i == 3:
            dim = re.search("dimensions: (.+)\n", line).group(1)
            dim = eval(dim)
        elif i == 4:
            dim_mapping = re.search("mapping: (.+)\n", line).group(1)
            dim_mapping = eval(dim_mapping)

    cube = NanoCube(dim, name=name, loc_granularity=gran)
    cube.count = count

    cube.dim_mapping = dim_mapping
    return cube


def _load_nodes(stream):
    nodes = dict()
    last_node = None

    for line in stream.readlines():
        line = line.encode('utf-8')
        if "s:" in line:
            table = TimeSerieTable.load(line)
            nodes[table.id] = table
        else:
            node = Node.load(line, nodes)
            nodes[node.id] = node
            last_node = node

    return last_node


def _dump_cube(cube, stream):
    res = u"name: '{0.name}'\ncount: {0.count}\ngran: {0.location_granularity}\n".format(cube)
    res += u"dimensions: {}\n".format(str(cube.dimensions))
    res += u"mapping: {}\n".format(str(cube.dim_mapping))
    stream.write(res)


def _dump_nodes(node, stream):
    if not isinstance(node, TimeSerieTable):
        for key in node.proper_children:
            _dump_nodes(node.proper_children[key], stream)

        if node.has_proper_content:
            _dump_nodes(node.proper_content, stream)

    return stream.write(node.dump())