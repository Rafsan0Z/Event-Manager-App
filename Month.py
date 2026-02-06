from DateList import DateList
from EventExceptions import test_month, test_day, date_dict, WrongDateException
import math

class Month(DateList):
    
    def __new__(cls, month_name):
        test_month(month_name)
        return super().__new__(cls)
    

    def __init__(self, month_name):
        self.month = month_name
        self.max_days = date_dict[month_name.lower().strip()]
        if not hasattr(self, 'days'):
            super().__init__()

    def __reduce__(self):
        return (Month, (self.month,), self.__getstate__())
    
    def __getstate__(self):
        return {
            #'month_name': self.month,
            'days': self.days
        }
    
    def __setstate__(self, state):
        #self.month = state['month_name']
        self.days = state['days']

    # def __insert_pos(self, day):
    #     self.check_day_type(day)
    #     if not len(self): return 0
    #     left_index = 0
    #     right_index = len(self) - 1
    #     mid_index = 0
    #     while left_index <= right_index:
    #         mid_index = math.floor((left_index + right_index) / 2)
    #         mid_day = self[mid_index]
    #         if mid_day.date_num < day.date_num:
    #             left_index = mid_index + 1
    #         elif mid_day.date_num > day.date:
    #             right_index = mid_index - 1
    #     return mid_index
    
    def __insert_pos(self, date):
        self.check_day_type(date)
        index = 0
        while index < len(self):
            if self[index].date_num >= date.date_num:
                break
            index += 1
        return index

    def __refactor_dates(self):
        # get the day for the first date of the month based on year
        # use that to calculate day names for each of the dates
        # rename the dates
        # everything else remains untouched
        pass

    def __setitem__(self, i, day):
        raise Exception("Month object can't have dates set to it, only inserted and appended!")

    def insert(self, i, day):
        assert len(self) <= self.max_days, "The month is already full"
        final_index = self.__insert_pos(day)
        if final_index != i and i != len(self):
            print("The index you provided is not correct, but we've inserted the day in the correct position")
        if self.year_num:
            try:
                test_day(day.day_name, self.month, self.year_num, day.date_num)
            except WrongDateException as w:
                self.__refactor_dates()

        self.give_month_to_days(day)
        self.days.insert(final_index, day)

    def give_month_to_days(self, day): 
        setattr(day, 'month_name', self.month)

    def __str__(self):
        result = "For {month}: \n".format(month = self.month)
        result += super().__str__()
        return result

#test = Month('January')
#print(test)
# print(test.month)


