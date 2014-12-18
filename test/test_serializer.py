import io
import os
from helpers import mock_cube
import libs.serializer as serializer
from nose.tools import ok_, eq_


class TestSerializer:
    def __init__(self):
        self.cube = mock_cube()

    def load_nano_file(self, name):
        file_path = os.path.dirname(__file__) + "/samples/{}.nano".format(name)
        with open(file_path) as sample_file:
            return sample_file.read()

    def test_dump_header(self):
        output = io.StringIO()
        serializer.dump_cube(self.cube, output)
        ret = output.getvalue()
        output.close()

        ok_("'cube'" in ret)
        ok_("['Devise']" in ret)
        ok_("'Android': '0'" in ret)
        ok_("'iPhone': '1'" in ret)

    def test_load_header(self):
        txt = self.load_nano_file('header')
        stream = io.StringIO(unicode(txt))
        cube = serializer.load_cube(stream)
        stream.close()

        eq_(cube.name, "Phone")
        eq_(cube.location_granularity, 10)
        eq_(cube.count, 5)
        eq_(cube.dimensions, ['Devise'])
        eq_(cube.dim_mapping, {'Devise': {'iPhone': 1, 'Android': 2}})


