from EventList import EventList
from EventExceptions import is_day, test_day, NotAnEventException

class Day(EventList):
    
    def __new__(cls, *args, **kwargs):
        is_day(args[1])
        test_day(args[1],args[0],args[3],args[2])
        return super().__new__(cls)

    def __init__(self, day_name):
        self.day_name = day_name
        super().__init__()

    def get_date_num(self):
        return self.date_num
    
    def set_date_num(self, num):
        self.date_num = num

    def __str__(self):
        result = "{day} {month} {date}\n".format(
            day = self.day_name,
            month = self.month_name,
            date = self.date_num
        )
        result += super().__str__()
        return result


class Date(Day):

    def __init__(self, day_name, date_num):
        self.date_num = date_num
        super().__init__(day_name)
        


#test = Day('January',"Saturday",31,2026)
#print(test)
# test.add_event("I promise is this an event")