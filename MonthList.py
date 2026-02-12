from collections.abc import MutableSequence
from EventExceptions import NotAMonthException
from Month import Month
from datetime import timedelta as dur
class MonthList(MutableSequence):

    def __init__(self):
        self.months = []
        self.size = 0
    
    def __len__(self):
        return len(self.months)

    def __getitem__(self, i):
        return self.months[i]

    def check_month_item(self, month_candidate):
        if not isinstance(month_candidate, Month):
            raise NotAMonthException(month_candidate)

    def __setitem__(self, i, month):
        self.check_month_item(month)
        self.months[i] = month

    def __delitem__(self, i):
        del self.months[i]

    def insert(self, i, month):
        self.check_month_item(month)
        self.months.insert(i, month)

    def add_month(self, month_candidate):
        if isinstance(month_candidate, str):
            new_month = Month(month_candidate)
            self.append(new_month)
        elif isinstance(month_candidate, Month):
            self.append(month_candidate)
        else:
            raise NotAMonthException(month_candidate)

    def give_months(self):
        for month in self.months:
            yield month

    def __iter__(self):
        return self.give_months()
    
    def __str__(self):
        result = ''
        for month in self.months:
            result += str(month)
        return result
    
    def num_events(self):
        count = 0
        for month in self.months:
            count += month.num_events()
        return count

    def total_duration(self):
        total = dur()
        for month in self.months:
            total += month.total_duration()
        return total
    
    def search_months(self, month_name = None):
        if not month_name: return self
        filtered = []
        for month in self.months:
            if month.month.lower() == month_name: filtered.append(month)
        return filtered