from collections.abc import MutableSequence
from Date import Date
from EventExceptions import NotADayException

class DateList(MutableSequence):
    
    def __init__(self):
        self.days = []
    
    def __len__(self):
        return len(self.days)
    
    def __getitem__(self, i):
        return self.days[i]

    def check_day_type(self, day_candidate):
        if not isinstance(day_candidate, Date):
            raise NotADayException(day_candidate)

    def __insert_pos(self, date):
        self.check_day_type(date)
        index = 0
        while index < len(self):
            if self[index].date_num >= date.date_num:
                break
            index += 1
        return index

    def __setitem__(self, i, date):
        self.check_day_type(date)
        final_pos = self.__insert_pos(date)
        if final_pos == len(self): final_pos -= 1
        self.days[final_pos] = date

    def __delitem__(self, i):
        del self.days[i]

    def insert(self, i, date):
        self.check_day_type(date)
        final_pos = self.__insert_pos(date)
        self.days.insert(final_pos, date)

    def num_events(self):
        total = 0
        for date in self.days:
            total += date.num_events()
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
    
    def search_days(self, day_name = None):
        if not day_name: return self
        filtered = []
        for day in self.days:
            if day.day_name == day_name: filtered.append(day)
        return filtered
    
# test = DateList()
# test.append(Date('Monday', 1))
# test.append(Date('Monday', 4))
# test.append(Date('Monday', 6))
# test.insert(0, Date('Monday', 10))
# print(test)
# test.insert(-1, Date('Monday', 3))
# print(test)