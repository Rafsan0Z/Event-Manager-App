from collections.abc import MutableSequence
from EventExceptions import NotAMonthException
from Month import Month
class MonthList(MutableSequence):

    def __init__(self):
        self.months = []
        self.size = 0
    
    def __len__(self):
        pass

    def __getitem__(self, i):
        pass

    def check_month_item(self, month_candidate):
        if isinstance(month_candidate, Month):
            raise NotAMonthException(month_candidate)

    def __setitem__(self, i, month):
        pass

    def __delitem__(self, i):
        pass

    def insert(self, i, month):
        pass

    def add_month(self, month_string):
        new_month = Month(month_string)
        self.append(new_month)
