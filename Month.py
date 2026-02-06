from DayList import DayList
from EventExceptions import test_month, test_day, date_dict
import math

class Month(DayList):
    
    def __new__(cls, month_name):
        test_month(month_name)
        return super().__new__(cls)
    

    def __init__(self, month_name):
        self.month = month_name
        self.max_days = date_dict[month_name.lower().strip()]
        super().__init__()

    def __insert_pos(self, day):
        self.check_day_type(day)
        if not len(self): return 0
        left_index = 0
        right_index = len(self) - 1
        mid_index = 0
        while left_index <= right_index:
            mid_index = math.floor((left_index + right_index) / 2)
            mid_day = self[mid_index]
            if mid_day.date_num < day.date_num:
                left_index = mid_index + 1
            elif mid_day.date_num > day.date:
                right_index = mid_index - 1
        return mid_index

    def __setitem__(self, i, day):
        raise Exception("Month object can't have days set to it, only inserted and appended!")

    def insert(self, i, day):
        assert len(self) <= self.max_days, "The month is already full"
        final_index = self.__insert_pos(day)
        if final_index != i and i != len(self):
            print("The index you provided is not correct, but we've inserted the day in the correct position")
        if self.year_num:
            test_day(day.day_name, self.month, self.year_num, day.date_num)
        self.give_month_to_days(day)
        self.insert(final_index, day)

    def give_month_to_days(self, day): 
        setattr(day, 'month_name', self.month)

    def __str__(self):
        result = "For {month}: \n".format(month = self.month)
        result += super().__str__()
        return result

#test = Month('January')
#print(test)
# print(test.month)


