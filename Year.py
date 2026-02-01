from MonthList import MonthList, Month

class Year(MonthList):

    def __init__(self, number):
        self.number = number
        self.__claimed_months = []
        super().__init__()
    
    def __setitem__(self, i, month):
        self.check_month_item(month)
        current_month_name = self[i].month

        if month.month in self.__claimed_months:
            if current_month_name != month.month:
                raise Exception("ERROR")
        else:
            self.__claimed_months.remove(current_month_name)
            self.__claimed_months.append(month.month)

        self.months[i] = month

    def insert(self, i, month):
        self.check_month_item(month)
        if month.month in self.__claimed_months:
            raise Exception("This month is already claimed!")
        else:
            self.__claimed_months.append(month.month)
            self.months.insert(i, month)

    def give_events(self):
        for month in self.months:
            for day in month.days:
                for event in day:
                    yield event

    def __str__(self): #will be changed
        result = ''
        for month in self.months:
            result += month.month + '\n'
        return result



# test = Year(2026)
# test.append(Month('january'))
# test.append(Month('february'))
# test.append(Month('march'))
# test[-1] = Month('april')
# test.append(Month('march'))
# print(test)
# print(test[0])