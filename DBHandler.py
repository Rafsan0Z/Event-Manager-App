import shelve
import matplotlib.pyplot as plt
import numpy as np
from EventExceptions import month_list

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
        for year in self.year_list.search_years(year_num):
            #print the year num here
            #print(year.number)
            for month in year.search_months(month_name):
                #print the month here
                #print(month.month)
                for date in month.search_days(day_name):
                    #print the day (and date number) here
                    #print(date.day_name, date.date_num)
                    for event in date:
                        #print the event here
                        print(event)

    def plot_events_date(self):
        xlist = []
        ylist = []
        for year in self.year_list:
            for month in year:
                for date in month:
                    date_string = str(date.date_num) + '/' + str(month_list.index(month.month.lower())) + '/' + str(year.number)[-2:]
                    xlist.append(date_string)
                    ylist.append(date.num_events())
        
        plt.figure(figsize=(len(xlist), 6))
        plt.xticks(rotation=45,ha='right')
        graph = plt.barh(xlist, ylist)
        plt.bar_label(graph)
        plt.ylim(0, max(ylist) * 1.2)
        plt.xlabel('Dates')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        plt.show()

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