import io
from helpers import mock_cube
import libs.serializer as serializer
from nose.tools import ok_


class TestSerializer:
    def __init__(self):
        self.cube = mock_cube()

    def test_dump_header(self):
        output = io.StringIO()
        serializer.dump_cube(self.cube, output)
        ret = output.getvalue()
        output.close()

        ok_("'cube'" in ret)
        ok_("['Devise']" in ret)
        ok_("'Android': '0'" in ret)
        ok_("'iPhone': '1'" in ret)

