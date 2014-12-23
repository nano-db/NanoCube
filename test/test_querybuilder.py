from datetime import datetime

from nose.tools import ok_, eq_

from helpers import mock_cube
from server.querybuilder import QueryBuilder


class TestQueryBuilder:
    def __init__(self):
        self.simple_cube = mock_cube()

    def test_count(self):
        cube = self.simple_cube
        count = QueryBuilder(cube).execute()
        eq_(count, 5)

    def test_enable_trace_in_constructor(self):
        cube = self.simple_cube
        q = QueryBuilder(cube, debug=True)
        q.execute()
        ok_(hasattr(q, 'trace'))

    def test_enable_trace_in_exec(self):
        cube = self.simple_cube
        q = QueryBuilder(cube)
        q.execute(debug=True)
        ok_(hasattr(q, 'trace'))

    def test_trace_count(self):
        cube = self.simple_cube
        q = QueryBuilder(cube)
        q.execute(debug=True)
        eq_(q.trace, [[], []])

    def test_trace_full(self):
        cube = self.simple_cube
        q = QueryBuilder(cube)\
            .find("Location", (["1,0", "11,01"], 0))\
            .find("Devise", cube.dim_mapping['Devise']['iPhone'])
        q.execute(debug=True)
        eq_(q.trace, [["1,0", "11,01"], []])

    def test_without_restriction(self):
        cube = self.simple_cube
        q = QueryBuilder(cube)\
            .find("Location", (["1,0"], 0))
        count = q.execute(debug=True)
        eq_(q.trace, [["1,0"], []])
        eq_(count, 2)

    def test_to_content(self):
        cube = self.simple_cube
        q = QueryBuilder(cube)\
            .find("Devise", cube.dim_mapping['Devise']['iPhone'])
        count = q.execute(debug=True)
        eq_(q.trace, [[], ["1"]])
        eq_(count, 3)

    def test_after(self):
        cube = self.simple_cube
        count = QueryBuilder(self.simple_cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .after(datetime(2014, 12, 10, 12, 30)).execute()
        eq_(count, 1)

        count = QueryBuilder(self.simple_cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .after(datetime(2014, 12, 10, 14, 30)).execute()
        eq_(count, 0)

    def test_before(self):
        cube = self.simple_cube
        count = QueryBuilder(self.simple_cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .before(datetime(2014, 12, 10, 12, 30)).execute()
        eq_(count, 1)

        count = QueryBuilder(self.simple_cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .before(datetime(2014, 12, 10, 14, 30)).execute()
        eq_(count, 2)

    def test_between(self):
        cube = self.simple_cube
        q = QueryBuilder(self.simple_cube)\
            .find("Devise", cube.dim_mapping['Devise']['Android'])\
            .between(datetime(2014, 12, 10, 12, 30), datetime(2014, 12, 10, 11, 30))
        try:
            q.execute()
        except Exception:
            pass
        else:
            ok_(False)

        count = QueryBuilder(self.simple_cube)\
            .between(datetime(2014, 12, 10, 9, 30), datetime(2014, 12, 10, 11, 30)).execute()
        eq_(count, 2)