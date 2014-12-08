from datetime import datetime
from nose.tools import assert_equals
from libs.timeserietable import TimeSerieTable


class TestTimeSerieTable(object):
    def mock_time(self, hour, min, sec):
        return datetime(2005, 7, 12, hour, min, sec)

    def test_simple_insert(self):
        t = TimeSerieTable(3600)
        d = self.mock_time(14, 12, 30)
        t.insert(d)

        assert_equals(t.start, d)
        assert_equals(len(t.table), 1)

        d = self.mock_time(14, 12, 40)
        t.insert(d)
        assert_equals(len(t.table), 1)
        assert_equals(t.table[len(t.table) - 1]['sum'], 2)

    def test_expand_at_beginning(self):
        t = TimeSerieTable(3600)
        t.insert(self.mock_time(14, 45, 30))
        t.insert(self.mock_time(13, 30, 45))

        assert_equals(t.start, self.mock_time(12, 45, 30))
        assert_equals(len(t.table), 3)
        assert_equals(t.table[0]['sum'], 1)
        assert_equals(t.table[len(t.table) - 1]['sum'], 2)
