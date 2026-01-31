from MonthList import Month_List as Months

class Year_List:

    def __init__(self, number):
        self.number = number
        self.months = []
        for i in range(1,13):
            self.months.append(Months())
    
    
    def give_months(self):
        for month in self.months:
            yield month
    
    def __iter__(self):
        return self.give_months()