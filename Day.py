from EventList import EventList
from EventExceptions import is_day, test_day, NotAnEventException
class Day(EventList):
    
    def __new__(cls, *args, **kwargs):
        is_day(args[1])
        test_day(args[1],args[0],args[3],args[2])
        return super().__new__(cls)

    def __init__(self, month_name, day_name, date_num, year_num):
        self.day_name = day_name
        self.date_num = date_num
        self.month_name = month_name
        self.year_num = year_num
        super().__init__()

    def get_date_num(self):
        return self.date_num

    def get_day_name(self):
        return self.day_name
    
    def set_date_num(self, num):
        self.date_num = num
    
    def set_day_name(self, day):
        self.day_name = day    

# test = Day('January',"Saturday",31,2026)
# test.add_event("I promise is this an event")