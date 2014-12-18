import io
import re
import json
from nanocube import NanoCube
from timeserietable import TimeSerieTable


def dump(cube):
    output = io.StringIO()

    dump_cube(cube, output)
    dump_nodes(cube.world, output)
    res = output.getvalue()

    output.close()
    return res


def load(string):
    stream = io.StringIO(string)
    cube = load_cube(stream)
    stream.close()
    return cube


def load_cube(stream):
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

    for dim in dim_mapping:
        for key in dim_mapping[dim]:
            val = dim_mapping[dim][key]
            dim_mapping[dim][key] = int(val)
    cube.dim_mapping = dim_mapping
    return cube


def dumps(cube, file_name):
    output = io.open(file_name, mode="w")
    dump_cube(cube, output)
    dump_nodes(cube.world, output)
    output.close()


def dump_cube(cube, stream):
    res = u"name: '{0.name}'\ncount: {0.count}\ngran: {0.location_granularity}\n".format(cube)
    res += u"dimensions: {}\n".format(str(cube.dimensions))
    res += u"mapping: {}\n".format(str(cube.dim_mapping))
    stream.write(res)


def dump_nodes(node, stream):
    if not isinstance(node, TimeSerieTable):
        for key in node.proper_children:
            dump_nodes(node.proper_children[key], stream)

        if node.has_proper_content:
            dump_nodes(node.proper_content, stream)

    return stream.write(node.dump())