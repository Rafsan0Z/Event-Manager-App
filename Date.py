from EventList import EventList
from EventExceptions import is_day, NotAnEventException

class Day(EventList):
    
    def __new__(cls, *args, **kwargs):
        is_day(args[0])
        #test_day(args[1],args[0],args[3],args[2])
        return super().__new__(cls)

    def __init__(self, day_name):
        self.day_name = day_name
        super().__init__()

    def __str__(self):
        result = "{day} \n".format(
            day = self.day_name
        )
        result += super().__str__()
        return result


class Date(Day):

    def __new__(cls, *args):
        assert args[-1] <= 31, "Date number is too high"
        return super().__new__(cls, args[0])

    def __init__(self, day_name, date_num):
        self.date_num = date_num
        super().__init__(day_name)

    def __str__(self):
        without_top_line = "\n".join(super().__str__().split('\n')[1:])
        new_top_line = "{day} {date}\n".format(
            day = self.day_name,
            date = self.date_num
        )
        return new_top_line + without_top_line


#test = Day('January',"Saturday",31,2026)
#print(test)
# test.add_event("I promise is this an event")
#test = Date("Wednesday", 40)