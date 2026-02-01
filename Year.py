from MonthList import MonthList, Month

class Year(MonthList):

    def __init__(self, number):
        self.number = number
        super().__init__()
    

    def give_events(self):
        for month in self.months:
            for day in month.days:
                for event in day:
                    yield event


# test = Year(2026)
# test.append(Month('january'))
# print(test[0])