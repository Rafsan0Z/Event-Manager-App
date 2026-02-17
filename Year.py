from MonthList import MonthList, Month

class Year(MonthList):

    def __init__(self, number):
        self.number = number
        self.__claimed_months = []
        super().__init__()
    
    def give_year_to_month(self, month):
        setattr(month, 'year_num', self.number)

    def __setitem__(self, i, month):
        self.check_month_item(month)
        current_month_name = self[i].month

        if month.month in self.__claimed_months:
            if current_month_name != month.month:
                raise Exception("ERROR")
        else:
            self.__claimed_months.remove(current_month_name)
            self.__claimed_months.append(month.month)

        self.give_year_to_month(month)
        self.months[i] = month

    def insert(self, i, month):
        self.check_month_item(month)
        if month.month in self.__claimed_months:
            raise Exception("This month is already claimed!")
        else:
            self.give_year_to_month(month)
            self.__claimed_months.append(month.month)
            self.months.insert(i, month)

    def add_event(self, event, month_name, day_name, date_num):
        target_month = self.find_month(month_name)
        if target_month:
            target_month.add_event(event, day_name, date_num)
        else:
            new_month = Month(month_name)
            self.append(new_month)
            new_month.add_event(event, day_name, date_num)

    def give_events(self):
        for month in self.months:
            for day in month.days:
                for event in day:
                    yield event
    
    def __str__(self):
        result = "--------------------------------{year}--------------------------------\n".format(
            year = self.number
        )
        result += super().__str__()
        return result

    def get_year_num(self):
        return self.number
    
    def get_month_names(self):
        return self.__claimed_months
