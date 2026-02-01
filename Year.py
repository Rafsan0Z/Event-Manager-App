from Month import Month
from MonthList import MonthList

class Year:

    def __init__(self, number):
        self.number = number
        self.months = MonthList()
    

    def add_month(self, month_name): 
        self.months.add_month(month_name)
    

    def give_events(self):
        for month in self.months:
            for day in month.days:
                for event in day:
                    yield event

    
    def give_months(self):
        for month in self.months:
            yield month
    
    def __iter__(self):
        return self.give_months()