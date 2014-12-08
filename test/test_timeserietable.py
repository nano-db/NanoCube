from datetime import datetime
from nose.tools import assert_equals
from libs.timeserietable import TimeSerieTable


class TestTimeSerieTable(object):
    def test_insert(self):
        t = TimeSerieTable(3600 * 60)
        d = datetime(2005, 7, 14, 12, 30)
        t.insert(d)

        assert_equals(t.start, d)
        assert_equals(len(t.table), 1)

        d = datetime(2005, 7, 14, 12, 37)
        t.insert(d)
        assert_equals(len(t.table), 1)
