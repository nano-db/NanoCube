class TimeSerieTable(object):
    def __init__(self, bin_size=1000):
        super(TimeSerieTable, self).__init__()
        self.start = None
        self.bin_size = bin_size
        self.table = []

    def insert(self, time):
        if len(self.table) == 0:
            self.start = time
            new_bin = {
                'count': 1,
                'sum': 1
            }
            self.table.append(new_bin)

        else:
            bin_num = (time - self.start) / self.bin_size
            self._expand_table(time, bin_num)

            self.table[bin_num]['sum'] += 1
            self.table[bin_num]['count'] += 1

            self._update_following_bins(bin_num)

    def _expand_table(self, time, bin_num):
        if bin_num > 0 and bin_num < len(self.table):
            return

        if bin_num < 0:
            for _ in range(abs(bin_num)):
                new_bin = {
                    'count': 0,
                    'sum': 0
                }
                self.table.insert(0, new_bin)
        else:
            final_sum = self.table[len(self.table)]['sum']
            final_count = self.table[len(self.table)]['count']
            for _ in range(bin_num - len(self.table)):
                new_bin = {
                    'count': final_count,
                    'sum': final_sum
                }
                self.table.append(new_bin)

    def _update_following_bins(self, bin_num):
        for i in range(bin_num + 1, len(self.table)):
            new_sum = self.table[i - 1]['sum'] + self.table[i]['count']
            self.table[i]['sum'] = new_sum

    def query(self, begin, end):
        begin_bin = (begin - self.start) / self.bin_size
        if begin_bin < 0:
            begin_bin = 0

        end_bin = (end - self.start) / self.bin_size
        if end_bin > self.start + len(self.table) * self.bin_size:
            end_bin = len(self.table) - 1

        return self.table[end_bin]['sum'] - self.table[begin_bin]['sum']
