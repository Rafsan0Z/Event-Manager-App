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
            self.year_list = db['YearList']
        db.close()
    
    def flush_to_database(self):
        with shelve.open("Event_DB") as db:
            db['YearList'] = self.year_list

    def grab_events(self, year_num = None, month_name = None, day_name = None, date_num = None):
        # new_list = YearList()
        for year in self.year_list.search_years(year_num):
            #print the year num here
            #print(year.number)
            # new_list.add_year(year)
            for month in year.search_months(month_name):
                #print the month here
                #print(month.month)
                for date in month.search_dates(day_name, date_num):
                    #print the day (and date number) here
                    #print(date.day_name, date.date_num)
                    for event in date:
                        #print the event here
                        print(event)

    def yesterdays_events(self):
        yesterday_year = datetime.now().year
        today_month = month_list[datetime.now().month - 1].lower().strip()
        today_date = datetime.now().day
        if today_date - 1 < 1:
            yesterday_month = month_list[datetime.now().month - 1]
            if datetime.now().month - 1 < 0: yesterday_year -= 1
            yesterday_date = date_dict[yesterday_month]
        else:
            yesterday_month = today_month
            yesterday_date = today_date - 1
        yesterday_day = days_list[days_list.index(datetime.now().strftime('%A').lower().strip()) - 1]
        self.grab_events(yesterday_year, yesterday_month, yesterday_day, yesterday_date)


    def todays_events(self):
        today_year = datetime.now().year
        today_month = month_list[datetime.now().month - 1]
        today_day = datetime.now().strftime('%A').strip()
        today_date = datetime.now().day
        self.grab_events(today_year, today_month, today_day, today_date)
    
    def tomorrows_events(self):
        tomorrow_year = datetime.now().year
        today_month = month_list[datetime.now().month - 1].lower().strip()
        today_date = datetime.now().day
        if today_date + 1 > date_dict[today_month]:
            tomorrow_month = month_list[datetime.now().month % 12]
            tomorrow_date = 1
        else:
            tomorrow_month = today_month
            tomorrow_date = today_date + 1
        tomorrow_day = days_list[(days_list.index(datetime.now().strftime('%A').lower().strip()) + 1) % 7]
        self.grab_events(tomorrow_year, tomorrow_month, tomorrow_day, tomorrow_date)

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
        


    def total_time(self):
        total = dur()
        for year in self.year_list:
            for month in year:
                for date in month:
                    total += date.total_duration()
        days = total.days
        remainder = total - dur(days=days)
        hours = 0
        mins = math.floor(remainder.seconds / 60)
        seconds = remainder.seconds - 60 * mins
        if mins > 60:
            hours = math.floor(mins / 60)
            mins -= hours * 60

        return "{days} days {hours} hours {mins} mins {seconds} seconds".format(
            days = days,
            hours = hours,
            mins = mins,
            seconds = seconds
        )

    def find_max_event_year(self):
        max_count = 0
        max_year = None
        for year in self.year_list:
            curr_year_count = year.num_events()
            if curr_year_count > max_count:
                max_count = curr_year_count
                max_year = year
        return max_year, max_count

    def find_max_event_month(self):
        max_count = 0
        max_month = None
        for year in self.year_list:
            for month in year:
                curr_month_count = month.num_events()
                if curr_month_count > max_count:
                    max_count = curr_month_count
                    max_month = month
        return max_month, max_count
    
    def find_max_event_date(self):
        max_count = 0
        max_date = None
        for year in self.year_list:
            for month in year:
                for date in month:
                    curr_date_count = date.num_events()
                    if curr_date_count > max_count:
                        max_count = curr_date_count
                        max_date = date
        return max_date, max_count                


    def plot_events(self, tag = 'date'):
        tag = tag.strip().lower()
        match tag:
            case 'date':
                self.plot_events_date()
            case 'month':
                self.plot_events_month()
            case 'year':
                self.plot_events_year()
        

    def plot_events_date(self):
        xlist = []
        ylist = []
        for year in self.year_list:
            for month in year:
                for date in month:
                    date_string = str(month_list.index(month.month.lower()) + 1) + '/' + str(date.date_num) + '/' + str(year.number)[-2:]
                    xlist.append(date_string)
                    ylist.append(date.num_events())
        
        #plt.figure(figsize=(len(xlist), 6))
        fig, ax = plt.subplots(figsize=(16,9))
        graph = ax.bar(xlist, ylist, color='gray')
        plt.bar_label(graph, labels=xlist, label_type='center', rotation=90, color='white')
        plt.bar_label(graph, label_type='edge')
        plt.xticks([])
        plt.ylim(0, max(ylist) * 1.2)
        plt.xlabel('Dates')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        plt.tight_layout()
        plt.show()
        return fig

    def plot_events_year(self):
        xlist = []
        ylist = []
        for year in self.year_list:
            xlist.append(str(year.number))
            ylist.append(year.num_events())
        xrange = np.array(xlist)
        yrange = np.array(ylist)
        graph = plt.bar(xlist, ylist)
        plt.bar_label(graph)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Years')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        plt.show()

    def plot_events_month(self):
        xlist = []
        ylist = []
        for year in self.year_list:
            for month in year:
                xlist.append(month.month[:3] + str(year.number)[-2:])
                ylist.append(month.num_events())
        xrange = np.array(xlist)
        yrange = np.array(ylist)
        #plt.plot(xrange, yrange)
        graph = plt.bar(xlist, ylist)
        plt.bar_label(graph)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Months')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        plt.show()

#test = DBFactory()
#print(test.year_list)
#test.grab_events(2026,'February', 'Wednesday')