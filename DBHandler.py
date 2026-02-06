import shelve

def DBFactory():
    try:
        new_handler = DBHandler()
    except RuntimeError as r:
        print("You cant request any more handlers!!")
    else:
        return new_handler


class DBHandler:
    
    num = 0

    def __new__(cls, *args, **kawrgs):
        if DBHandler.num > 0:
            raise RuntimeError("You cannot create any more Database Handlers")
        else:
            return super().__new__(cls)
        
    def __init__(self):
        self.read_from_database()
        DBHandler.num += 1

    def __del__(self):
        #self.flush_to_database()
        DBHandler.num -= 1

    def read_from_database(self):
        with shelve.open("Event_DB") as db:
            #print(db['YearList'])
            self.year_list = db['YearList']
        db.close()
    
    def flush_to_database(self):
        with shelve.open("Event_DB") as db:
            db['YearList'] = self.year_list

    def grab_events(self, year_num = None, month_name = None, day_name = None, date_num = None):
        for year in self.year_list.search_years(year_num):
            #print the year num here
            for month in year.search_months(month_name):
                #print the month here
                for date in month.search_days(day_name):
                    #print the day (and date number) here
                    for event in date:
                        #print the event here
                        pass
    

test = DBFactory()
print(test.year_list)