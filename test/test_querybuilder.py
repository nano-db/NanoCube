from nose.tools import assert_equals
from helpers import mock_cube
from libs.querybuilder import QueryBuilder


class TestQueryBuilder:
    def test_count(self):
        cube = mock_cube()
        count = QueryBuilder(cube).execute()
        assert_equals(count, 5)

    def test_enable_trace_in_constructor(self):
        cube = mock_cube()
        q = QueryBuilder(cube, debug=True)
        q.execute()
        assert(hasattr(q, 'trace'))

    def test_enable_trace_in_exec(self):
        cube = mock_cube()
        q = QueryBuilder(cube)
        q.execute(debug=True)
        assert(hasattr(q, 'trace'))

    def test_trace_count(self):
        cube = mock_cube()
        q = QueryBuilder(cube)
        q.execute(debug=True)
        assert_equals(q.trace, [[], []])

    def test_trace_full(self):
        cube = mock_cube()
        q = QueryBuilder(cube)\
            .find("Location", (["1,0", "11,01"], 0))\
            .find("Devise", cube.dim_mapping['Devise']['iPhone'])
        q.execute(debug=True)
        assert_equals(q.trace, [["1,0", "11,01"], []])

    def test_without_restriction(self):
        cube = mock_cube()
        q = QueryBuilder(cube)\
            .find("Location", (["1,0"], 0))
        count = q.execute(debug=True)
        assert_equals(q.trace, [["1,0"], []])
        assert_equals(count, 2)

    def test_to_content(self):
        cube = mock_cube()
        q = QueryBuilder(cube)\
            .find("Devise", cube.dim_mapping['Devise']['iPhone'])
        count = q.execute(debug=True)
        assert_equals(q.trace, [[], ["1"]])
        assert_equals(count, 3)