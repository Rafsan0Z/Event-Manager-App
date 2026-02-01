from Month import Month

class Year:

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