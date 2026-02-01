from Month import Month

class Year_List:

    def __init__(self, number):
        self.number = number
        self.months = []
    

    def add_month(self, month_name):
        try:
            new_month = Month(month_name)
        except Exception as e:
            print(e)
        else:
            self.months.append(new_month)
    
    
    def give_months(self):
        for month in self.months:
            yield month
    
    def __iter__(self):
        return self.give_months()