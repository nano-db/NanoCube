import io
from timeserietable import TimeSerieTable


def dump(cube):
    output = io.StringIO()

    dump_cube(cube, output)
    dump_nodes(cube.world, output)
    res = output.getvalue()

    output.close()
    return res


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