from nose.tools import assert_equals
from helpers import mock_cube
from libs.querybuilder import QueryBuilder

class TestQueryBuilder:
    def test_count(self):
        cube = mock_cube()
        count = QueryBuilder(cube).execute()
        assert_equals(count, 5)


