from collections.abc import MutableSequence
from Day import Day
from EventExceptions import NotADayException

class DayList(MutableSequence):
    
    def __init__(self):
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

    def __str__(self):
        result = ''
        for day in self.days:
            result += "--------------------------------\n"
            result += str(day)
            result += "--------------------------------\n"
        return result

    def __day_search(self, day):
        pass

    def add_day(self, day): #This should input the day in a sorted manner
        pass

    def give_days(self):
        for day in self.days:
            yield day
    
    def __iter__(self):
        return self.give_days()
    
    def search_days(self, day_name):
        filtered = []
        for day in self.days:
            if day.day_name == day_name: filtered.append(day)
        if len(filtered):
            return filtered
        else:
            return self.give_days()