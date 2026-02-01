from collections.abc import MutableSequence
from Day import Day
from EventExceptions import date_dict

class DayList(MutableSequence):
    
    def __init__(self, month_name):
        self.month_name = month_name
        self.max_days = date_dict[month_name.lower().strip()]
        self.days = []
    
    def __len__(self):
        return len(self.days)
    
    def __getitem__(self, i):
        pass

    def __setitem__(self, i, day):
        pass

    def __delitem__(self, i):
        pass

    def insert(self, i, day):
        pass

    def __day_search(self, day):
        pass

    def add_day(self, day): #This should input the day in a sorted manner
        pass

    