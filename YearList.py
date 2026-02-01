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
        if isinstance(year_candidate, Year):
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


