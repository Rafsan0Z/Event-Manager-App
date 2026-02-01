from Event import Event
from Day import Day
from DayList import DayList
from EventExceptions import test_month

class Month:
    
    def __new__(cls, month_name):
        test_month(month_name)
        return super().__new__(cls)
    

    def __init__(self, month_name):
        self.month = month_name
        self.days = DayList(month_name)

    def num_events(self):
        total = 0
        for day in self.days:
            total += day.num_events()
        return total
    
    def isDayIncluded(self):
        pass

    def add_day(self):
        assert self.days <= 31, "There are too many days"
        pass

    def __str__(self):
        result = self.month + '\n'
        for day in self.days:
            result += "------------------------------\n"
            result += "For the day {name}:\n".format(name=day.get_day_name() + " " + day.get_date_num())
            event_index = 0
            for event in day:
                result += "{index}. {detail}\n".format(index=event_index+1, detail=event)
            result += "------------------------------\n"



# test = Month('January')
# print(test.month)


