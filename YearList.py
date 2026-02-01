from collections.abc import MutableSequence
class YearList(MutableSequence):

    def __init__(self):
        self.years = []
        self.size = 0
    
    def __len__(self):
        return len(self.years)
    
    def __getitem__(self, i):
        return self.years[i]
    
    def __setitem__(self, i, year):
        self.years[i] = year
    
    def __delitem__(self, i):
        del self.years[i]
    
    def insert(self, i, year):
        self.years.insert(i,year)
    
    def add_year(self, year):
        self.append(year)


