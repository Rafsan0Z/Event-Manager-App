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
        self.flush_to_database()
        DBHandler.num -= 1

    def read_from_database(self):
        with shelve.open("Event_DB", 'r') as db:
            self.year_list = db['YearList']
    
    def flush_to_database(self):
        with shelve.open("Event_DB") as db:
            db['YearList'] = self.year_list

    def grab_events(year_num = None, month_name = None, day_name = None, date_num = None):
        if year_num:
            if month_name:
                if date_num:
                    pass
                    # get it from self.year_list[year_num].get_month(month_name)[date_num]
                    # if the above doesn't match then we return nothing
                else:
                    pass
            else:
                pass
        else:
            pass
    
