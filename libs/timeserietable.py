import copy
import sys
from math import floor
from datetime import timedelta


class TimeSerieTable(object):
    def __init__(self, bin_size=3600):
        super(TimeSerieTable, self).__init__()
        self.start = None
        self.bin_size = bin_size
        self.table = []

    def insert(self, time):
        """ Insert an event into the table

        :param time: datetime time to insert
        :return:
        """
        if len(self.table) == 0:
            self.start = time
            new_bin = {
                'count': 1,
                'sum': 1
            }
            self.table.append(new_bin)

        else:
            bin_num = self._get_bin_number(time)
            self._expand_table(bin_num)

            if bin_num < 0:
                bin_num = 0

            self.table[bin_num]['sum'] += 1
            self.table[bin_num]['count'] += 1

            self._update_following_bins(bin_num)

    def _get_bin_number(self, time):
        """Return the bin index for the specified type

        :param time: datetime
        :rtype : int
        """
        delta = (time - self.start).total_seconds() / self.bin_size
        return int(floor(delta))

    @property
    def end(self):
        """Return the max time of the timetable"""
        if self.start is None:
            return None
        else:
            nb_sec = (len(self.table) * self.bin_size)
            return timedelta(seconds=nb_sec) + self.start

    def _expand_table(self, bin_num):
        """Expand the current time table to accept new insertion

        :param bin_num: int expected index
        """
        if 0 <= bin_num < len(self.table):
            return

        if bin_num < 0:
            diff_sec = bin_num * self.bin_size
            self.start = self.start + timedelta(seconds=diff_sec)
            for _ in range(abs(bin_num)):
                new_bin = {
                    'count': 0,
                    'sum': 0
                }
                self.table.insert(0, new_bin)
        else:
            final_sum = self.table[len(self.table) - 1]['sum']
            for _ in range(bin_num - len(self.table) + 1):
                new_bin = {
                    'count': 0,
                    'sum': final_sum
                }
                self.table.append(new_bin)

    def _update_following_bins(self, bin_num):
        """Update the table starting at the bin_num index

        :param bin_num: int
        """
        for i in range(bin_num + 1, len(self.table)):
            new_sum = self.table[i - 1]['sum'] + self.table[i]['count']
            self.table[i]['sum'] = new_sum

    def all(self):
        last_index = len(self.table) - 1
        return self.table[last_index]['sum']

    def after(self, date):
        if date > self.end:
            return 0
        else:
            last_index = len(self.table) - 1
            begin_bin = self._get_bin_number(date)
            if begin_bin <= 0:
                return self.table[last_index]['sum']
            elif begin_bin < len(self.table):
                return self.table[last_index]['sum'] - self.table[begin_bin - 1]['sum']
            else:
                return 0

    def before(self, date):
        if date < self.start:
            return 0
        else:
            last_index = len(self.table) - 1
            end_bin = self._get_bin_number(date)
            if end_bin >= len(self.table):
                return self.table[last_index]['sum']
            elif end_bin > 0:
                return self.table[end_bin - 1]['sum']
            else:
                return 0

    def between(self, begin, end):
        if begin > end:
            raise Exception("Impossible to date query: {0}-{1}".format(begin, end))

        begin_bin = self._get_bin_number(begin)
        end_bin = self._get_bin_number(end)
        if end_bin >= len(self.table):
            end_bin = len(self.table) - 1

        if begin_bin <= 0:
            return self.table[end_bin]['sum']
        else:
            return self.table[begin_bin - 1]['sum'] - self.table[end_bin]['sum']

    def query(self, begin, end):
        if begin is None and end is None:
            return self.all()
        elif begin is None:
            return self.before(end)
        elif end is None:
            return self.after(begin)
        else:
            return self.between(begin, end)


    def copy(self):
        """Return a shallow copy of the instance

        :return: TimeSerieTable
        """
        table_copy = copy.copy(self)
        table_copy.table = []
        for elem in self.table:
            table_copy.table.append(copy.copy(elem))
        return table_copy


    def __sizeof__(self):
        size = sys.getsizeof(self.start) + sys.getsizeof(self.bin_size)
        size += sys.getsizeof(self.table)
        return size
