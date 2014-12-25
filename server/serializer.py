import io
import json
import logging
import cStringIO
from .nanocube import NanoCube
from .node import Node
from .timeserietable import TimeSerieTable


def dumps(cube):
    '''Serialize a cube and return the string'''
    return _dumper(cube)


def dump(cube, file_name):
    '''Serialize a cube and write it to the passed file'''
    stream = open(file_name, mode="w")
    res = _dumper(cube)
    stream.write(res)
    stream.close()


def _dumper(cube):
    logger = logging.getLogger("nanoDB.serializer." + cube.name)
    logger.info("Start serialization")
    res = _dump_cube(cube)
    _dump_nodes(cube.world, res)
    res = '\n'.join(res)
    logger.info("End serialization")
    return res


def loads(string):
    '''Unserialize a cube from the passed string and return it'''
    stream = cStringIO.StringIO(string)
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
        line = line.rstrip()
        if i == 0:
            name = line
        elif i == 1:
            count = int(line)
        elif i == 2:
            gran = int(line)
        elif i == 3:
            dim = line.split(',')
        elif i == 4:
            dim_mapping = json.loads(line)

    cube = NanoCube(dim, name=name, loc_granularity=gran)
    cube.count = count

    cube.dim_mapping = dim_mapping
    return cube


def _load_nodes(stream):
    nodes = dict()
    last_node = None

    for line in stream.readlines():
        line = line.encode('utf-8')
        obj = line.rstrip().split('|')
        if obj[0] == 't':
            table = TimeSerieTable.load(obj[1:])
            nodes[table.id] = table
        else:
            node = Node.load(obj[1:], nodes)
            nodes[node.id] = node
            last_node = node

    return last_node


def _dump_cube(cube):
    return [
        cube.name,
        str(cube.count),
        str(cube.location_granularity),
        ','.join(cube.dimensions),
        json.dumps(cube.dim_mapping)
    ]


def _dump_nodes(node, res):
    if not isinstance(node, TimeSerieTable):
        for key in node.proper_children:
            _dump_nodes(node.proper_children[key], res)

        if node.has_proper_content:
            _dump_nodes(node.proper_content, res)

    return res.append(node.dump())