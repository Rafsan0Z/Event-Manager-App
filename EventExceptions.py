from datetime import date
days_list = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]
month_list = [
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december'
    ]
date_dict = {
        'january': 31,
        'february': 28,
        'march': 31,
        'april': 30,
        'may': 31,
        'june': 30,
        'july': 31,
        'august': 31,
        'september': 30,
        'october': 31,
        'november': 30,
        'december': 31
    }


class BadMonthException(Exception):

    def __init__(self, message, month_name):
        self.month_name = month_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{message}: {month_name}".format(
            message=self.message, 
            month_name=self.month_name
        )


class NotRealDayException(Exception):

    def __init__(self, day_name):
        self.message = "This is not a correct day name"
        self.day_name = day_name
        super().__init__(self.message)

    def __str__(self):
        return "{message}: {day_name}".format(
            message = self.message,
            day_name = self.day_name
        )

class WrongDayException(Exception):

    def __init__(self, message, wrong_day, real_day):
        self.message = message
        self.wrong_day = wrong_day
        self.real_day = real_day
        super().__init__(self.message)

    def __str__(self):
        return "{message}: {wrong} is wrong, correct day is {real}".format(
            message=self.message,
            wrong=self.wrong_day,
            real=self.real_day   
        )

class WrongDateException(Exception):

    def __init__(self, message, date_num):
        self.message = message
        self.date_num = date_num
        super().__init__(self.message)        

    def __str__(self):
        return "{message}: {date}".format(
            message=self.message, 
            date=self.date_num
        )

class WrongTypeException(Exception):

    def __init__(self, other_type, this_type = None):
        self.other_type = other_type
        if this_type: 
            self.this_type = this_type
        else:
            self.this_type = type(self)
        self.message = "Not an instance of a " + this_type + " class"
        super().__init__(self.message)

    def __str__(self):
        return "{message}: But of {other} instead".format(
            message = self.message,
            other = type(self.other_type)
        )

class NotAnEventException(WrongTypeException):

    def __init__(self, instance):
        super().__init__(instance, "Event")

class NotAMonthException(WrongTypeException):
    
    def __init__(self, instance):
        super().__init__(instance, "Month")

class NotAnYearException(WrongTypeException):
    
    def __init__(self, instance):
        super().__init__(instance, "Year")

def lower_strings(*strings):
    if len(strings) == 1:
        return strings[0].lower().strip()
    else:
        return [string.lower().strip() for string in strings]


def is_day(day_name):
    day_name = lower_strings(day_name)
    if day_name in days_list:
        return True
    else:
        raise NotRealDayException(day_name)

def test_month(month_name):
    month_name = lower_strings(month_name)
    if month_name in month_list:
        return True
    else:
        raise BadMonthException("The month does not exist!", month_name)

def test_date(month_name, date_num):
    month_name = lower_strings(month_name)
    test_month(month_name)
    if 1 <= date_num <= date_dict[month_name]:
        return True
    else:
        raise WrongDateException("The given date is out of range for the given month", date_num)

def test_day(day_name, month_name, year_num, date_num):
    month_name, day_name = lower_strings(month_name, day_name)
    test_month(month_name)
    test_date(month_name, date_num)
    comparison_day = date(year_num, month_list.index(month_name) + 1,date_num).strftime("%A").lower().strip()
    if comparison_day != day_name:
        raise WrongDayException("The day is wrong for the given year, month and date", day_name, comparison_day)
    else:
        return True
    
#test_month("MakeUpMonth")
#test_date('february', 28)
#test_day("friday", 'february', 2026, 28)

#raise NotAnEventException("oops")
#raise NotAnYearException(1003)
#raise NotAMonthException(True)