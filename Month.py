from Event import Event
from Day import Day
from DayList import DayList
from EventExceptions import test_month, date_dict

class Month(DayList):
    
    def __new__(cls, month_name):
        test_month(month_name)
        return super().__new__(cls)
    

    def __init__(self, month_name):
        self.month = month_name
        self.max_days = date_dict[month_name.lower().strip()]
        self.days = DayList()

    def add_day(self):
        assert len(self.days) > self.max_days, "There are too many days"
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


