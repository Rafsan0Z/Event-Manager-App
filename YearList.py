from collections.abc import MutableSequence
from Year import Year
from EventExceptions import NotAnYearException
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


