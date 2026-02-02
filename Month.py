from Event import Event
#from Day import Day
from DayList import DayList
from EventExceptions import test_month, date_dict

class Month(DayList):
    
    def __new__(cls, month_name):
        test_month(month_name)
        return super().__new__(cls)
    

    def __init__(self, month_name):
        self.month = month_name
        self.max_days = date_dict[month_name.lower().strip()]
        #self.days = DayList()
        super().__init__()

    def add_day(self):
        assert len(self.days) > self.max_days, "There are too many days"
        pass

    def __str__(self):
        result = "For {month}: \n".format(month = self.month)
        result += super().__str__()
        return result

#test = Month('January')
#print(test)
# print(test.month)


