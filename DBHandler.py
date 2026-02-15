import shelve
import matplotlib.pyplot as plt
import numpy as np
from EventExceptions import month_list, date_dict, days_list
from datetime import timedelta as dur
from datetime import datetime
import math

def DBFactory():
    try:
        new_handler = DBHandler()
    except RuntimeError as r:
        print("You cant request any more handlers!!")
    else:
        return new_handler


def isHandler(instance):
    return isinstance(instance, DBHandler)

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

    def getYearList(self):
        return self.year_list

    def read_from_database(self):
        with shelve.open("Event_DB") as db:
            self.year_list = db['YearList']
        db.close()
    
    def flush_to_database(self):
        with shelve.open("Event_DB") as db:
            db['YearList'] = self.year_list

    def total_time_watched(self):
        total = dur()
        today = datetime.now()
        today_year = today.year
        today_month = today.month
        today_date = today.day
        year_gen = self.year_list.give_years()
        year = next(year_gen)
        while year.number < today_year:
            # get the total time for the years that are not this one
            year = next(year_gen)
        # Now we're going through the current year months
        month_gen = year.give_months()
        month = next(month_gen)
        while month_list.index(month.month.lower()) < today_month:
            #get the total time for the months that are not the current
            month = next(month_gen)
        # Now we're going through the current month dates


    def total_upcoming_time(self):
        total = dur()
        today = datetime.now()
        today_year = today.year
        today_month = today.month
        today_date = today.day    