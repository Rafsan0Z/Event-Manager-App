from collections.abc import MutableSequence
from EventExceptions import NotAMonthException
from Month import Month
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

    def add_month(self, month_string):
        new_month = Month(month_string)
        self.append(new_month)

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
    
    def search_months(self, month_name = None):
        if not month_name: return self
        filtered = []
        for month in self.months:
            if month.month == month_name: filtered.append(month)
        return filtered