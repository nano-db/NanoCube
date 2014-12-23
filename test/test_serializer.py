import os
from datetime import datetime

from nose.tools import eq_

from helpers import mock_cube
from server.querybuilder import QueryBuilder
import server.serializer as serializer


class TestSerializer:
    def __init__(self):
        self.cube = mock_cube()

    def load_nano_file(self, name):
        file_path = os.path.dirname(__file__) + "/samples/{}.nano".format(name)
        with open(file_path) as sample_file:
            return sample_file.read()

    def cube_query(self, cube):
        eq_(cube.name, 'cube')
        eq_(cube.count, 5)
        eq_(cube.location_granularity, 2)
        eq_(cube.dimensions, ['Devise'])

        count = QueryBuilder(cube).execute()
        eq_(count, 5)

        count = QueryBuilder(cube)\
            .find("Devise", cube.dim_mapping['Devise']['iPhone'])\
            .execute()
        eq_(count, 3)

        count = QueryBuilder(cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .execute()
        eq_(count, 2)

        count = QueryBuilder(cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .before(datetime(2014, 12, 10, 12, 30)).execute()
        eq_(count, 1)

    def test_dump_and_load_simple(self):
        cube = mock_cube()
        ret = serializer.dumps(cube)
        loaded_cube = serializer.loads(ret)

        self.cube_query(cube)
        self.cube_query(loaded_cube)
