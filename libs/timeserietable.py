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

    def query(self, begin, end):
        """Calculate the number of event during the specified timeframe

        :param begin:  datetime beginning of the timeframe
        :param end: datetime end of the timeframe
        :return: int
        """
        if end is None:
            end_bin = len(self.table) - 1
        else:
            end_bin = self._get_bin_number(end)
            if end_bin < 0:
                end_bin = 0
            elif end_bin >= len(self.table):
                end_bin = len(self.table) - 1


        if begin is None:
            return self.table[end_bin]['sum']
        else:
            start_bin = self._get_bin_number(begin)
            if start_bin < 0:
                start_bin = 0
            elif start_bin >= len(self.table):
                start_bin = len(self.table) - 1

        if start_bin > end_bin:
            raise Exception("Begin date is after end date")
        else:
            return self.table[end_bin]['sum'] - self.table[start_bin]['sum']


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
