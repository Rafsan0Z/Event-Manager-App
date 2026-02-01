from collections.abc import MutableSequence
from Day import Day

class DayList(MutableSequence):
    
    def __init__(self):
        #self.month_name = month_name
        #self.max_days = date_dict[month_name.lower().strip()]
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

    def isDayIncluded(self, day):
        pass

    def num_events(self):
        total = 0
        for day in self.days:
            total += day.num_events()
        return total

    def __day_search(self, day):
        pass

    def add_day(self, day): #This should input the day in a sorted manner
        pass

    