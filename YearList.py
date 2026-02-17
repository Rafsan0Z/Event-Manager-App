from collections.abc import MutableSequence
from Year import Year
from Event import Event
from EventList import EventList
from EventExceptions import NotAnYearException
from datetime import timedelta as dur
class YearList(MutableSequence):

    def __init__(self):
        self.years = []
    
    def __len__(self):
        return len(self.years)
    
    def __getitem__(self, i):
        return self.years[i]

    def check_year_type(self, year_candidate):
        if not isinstance(year_candidate, Year):
            raise NotAnYearException(year_candidate)
    
    def __setitem__(self, i, year):
        self.check_year_type(year)
        self.years[i] = year
    
    def __delitem__(self, i):
        del self.years[i]
    
    def insert(self, i, year):
        self.check_year_type(year)
        self.years.insert(i,year)
    
    def add_year(self, year):
        self.check_year_type(year)
        self.append(year)

    def __str__(self):
        result = "--------------------------------Collection of All Events--------------------------------\n"
        for year in self.years:
            result += str(year)
        return result
    
    def search_years(self, year_num = None):
        if not year_num: return self
        filtered = []
        for year in self.years:
            if year.number == year_num: filtered.append(year)
        return filtered
    
    def find_year(self, year_num):
        for year in self.years:
            if year.number == year_num: return year

    def add_event(self, event, year_num, month_name, day_name, date_num):
        target_year = self.find_year(year_num)
        target_year.add_event(event, month_name, day_name, date_num)

    
    def num_events(self):
        count = 0
        for year in self.years:
            count += year.num_events()
        return count
    
    def num_days(self):
        count = 0
        for year in self.years:
            for month in year:
                count += len(month)
        return count
    
    def num_months(self):
        count = 0
        for year in self.years:
            count += len(year)
        return count
    
    def total_duration(self):
        total = dur()
        for year in self.years:
            total += year.total_duration()
        return total


    def give_years(self, reverse = False):
        for year in self.years:
            yield year
    
    def __iter__(self):
        return self.give_years()
    
    def grab_events(self, year_num = None, month_name = None, day_name = None, date_num = None): #send this to yearlist
        return_list = EventList()
        event_index = 1
        for year in self.search_years(year_num):
            #print the year num here
            print(f'For {year.number}')
            for month in year.search_months(month_name):
                #print the month here
                print(f'For {month.month}')
                for date in month.search_dates(day_name, date_num):
                    #print the day (and date number) here
                    print(f'For {date.day_name} the {date.date_num}')
                    for event in date:
                        #print the event here
                        print(f'({event_index}) {event}')
                        return_list.append(event)
                        event_index += 1
        return return_list



