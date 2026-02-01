from collections.abc import MutableSequence
from Day import Day
from EventExceptions import NotADayException

class DayList(MutableSequence):
    
    def __init__(self):
        #self.month_name = month_name
        #self.max_days = date_dict[month_name.lower().strip()]
        self.days = []
    
    def __len__(self):
        return len(self.days)
    
    def __getitem__(self, i):
        return self.days[i]

    def check_day_type(self, day_candidate):
        if not isinstance(day_candidate, Day):
            raise NotADayException(day_candidate)

    def __setitem__(self, i, day):
        self.check_day_type(day)
        self.days[i] = day

    def __delitem__(self, i):
        del self.days[i]

    def insert(self, i, day):
        self.check_day_type(day)
        self.days.insert(i, day)

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

    