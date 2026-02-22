from DBHandler import isHandler
from datetime import datetime, date, timedelta as dur
from dotenv import load_dotenv
from EventExceptions import month_list, date_dict, days_list
import numpy as np
import matplotlib.pyplot as plt
import calendar
import math
import os

class DateFuncs:

    def __init__(self, db_handler):
        if isHandler(db_handler):
            self.year_list = db_handler.getYearList()

    def getMaxDays(self, month):
        return date_dict[month.lower().strip()]

    def getListofYears(self):
        result = []
        for year in self.year_list:
            result.append(year.number)
        return result
    
    def getListofMonths(self, year_num):
        result = []
        for year in self.year_list.search_years(year_num):
            for month in year:
                result.append(month.month)
        return result
    
    def getFullListofMonths(self):
        return month_list
    
    def getFullListofDays(self):
        return days_list
    
    def getListofDates(self, year_num, month_name, day_name):
        result = []
        for day in range(1, date_dict[month_name.lower()]):
            target_date = date(year_num, month_list.index(month_name.lower()) + 1, day)
            if target_date.weekday() == days_list.index(day_name.lower()):
                result.append(day)
        return result

class InfoFuncs:

    def __init__(self, db_handler):
        if isHandler(db_handler):
            self.year_list = db_handler.getYearList()
        load_dotenv(override=True)

    def getDocName(self):
        return os.getenv('FILE_NAME')
    
    def getLastModTime(self):
        return os.getenv("LAST_MODIFIED")
    
    def getGithubLink(self):
        return os.getenv("GITHUB_URL")
    
    def getDocPullTime(self):
        return os.getenv("DOCUMENT_PULL_TIME")
    
    def getNumofYears(self):
        return len(self.year_list)
    
    def getNumofMonths(self):
        return self.year_list.num_months()
    
    def getNumofDays(self):
        return self.year_list.num_days()
    
    def getNumofEvents(self):
        return self.year_list.num_events()
    
    
    def getTodaysEvents(self):
        today_year = datetime.now().year
        today_month = month_list[datetime.now().month - 1]
        today_day = datetime.now().strftime('%A').strip()
        today_date = datetime.now().day
        self.year_list.grab_events(today_year, today_month, today_day, today_date)

    def getTomorrowsEvents(self): # Send this to yearlist
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
        self.year_list.grab_events(tomorrow_year, tomorrow_month, tomorrow_day, tomorrow_date)

    def getYesterdaysEvents(self): #send this to yearlist
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
        self.year_list.grab_events(yesterday_year, yesterday_month, yesterday_day, yesterday_date)

class StatFuncs:

    def __init__(self, db_handler):
        if isHandler(db_handler):
            self.year_list = db_handler.getYearList()

    def total_time_watched(self):
        pass

    def total_time_upcoming(self):
        pass

    def total_time(self):
        total = self.year_list.total_duration()
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

class PlotFuncs:

    def __init__(self, db_handler):
        if isHandler(db_handler):
            self.year_list = db_handler.getYearList()
    
    def finalize_time_labels(self, time_list):
        max_seconds = min([time.total_seconds() for time in time_list])
        unit = 'secs'
        ylist = [time.total_seconds() for time in time_list]
        if max_seconds > 60 * 2:
            unit = 'mins'
            ylist =  [time.seconds / 60 for time in time_list]
        if max_seconds > 60 * 60 * 1.5:
            unit = 'hours'
            ylist = [time.seconds / (60 * 60) for time in time_list]
        if max_seconds > 60 * 60 * 24 * 1.5:
            unit = 'days'
            ylist = [time.seconds / (60 * 60 * 24) for time in time_list]
        
        labels = [f" {time:.2f}" for time in ylist]
        return ylist, labels, unit
    
    def plot_events_year(self):
        xlist = []
        ylist = []
        for year in self.year_list:
            xlist.append(str(year.number))
            ylist.append(year.num_events())
        #xrange = np.array(xlist)
        #yrange = np.array(ylist)
        fig, ax = plt.subplots()
        graph = ax.bar(xlist, ylist)
        plt.bar_label(graph)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Years')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        return plt, fig
    
    def plot_events_month(self, year_num = None):
        xlist = []
        ylist = []
        if year_num: years = self.year_list.search_years(year_num)
        else: years = self.year_list
        for year in years:
            for month in year:
                xlist.append(month.month[:3] + str(year.number)[-2:])
                ylist.append(month.num_events())
        #xrange = np.array(xlist)
        #yrange = np.array(ylist)
        fig, ax = plt.subplots()
        graph = ax.bar(xlist, ylist)
        plt.bar_label(graph)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Months')
        plt.ylabel('# of Events')
        plt.title('Event Plot')
        return plt, fig
    
    def plot_events_date(self, year_num = None, month_name = None):
        xlist = []
        ylist = []
        if year_num: years = self.year_list.search_years(year_num)
        else: years = self.year_list
        for year in years:
            if month_name: months = year.search_months(month_name)
            else: months = year
            for month in months:
                for date in month:
                    date_string = str(month_list.index(month.month.lower()) + 1) + '/' + str(date.date_num) + '/' + str(year.number)[-2:]
                    xlist.append(date_string)
                    ylist.append(date.num_events())
        
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
        return plt, fig

    def plot_time_year(self):
        time_list = []
        xlist = []
        for year in self.year_list:
            year_time = year.total_duration()
            if year_time: 
                time_list.append(year_time)
                xlist.append(str(year.number))
        
        ylist, labels, unit = self.finalize_time_labels(time_list)
        fig, ax = plt.subplots()
        graph = ax.bar(xlist, ylist)
        plt.bar_label(graph, labels=labels)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Years')
        plt.ylabel(f'Time in {unit}')
        plt.title('Event Time Plot')
        return plt, fig

    def plot_time_month(self, year_num = None):
        time_list = []
        xlist = []
        if year_num: years = self.year_list.search_years(year_num)
        else: years = self.year_list
        for year in years:
            for month in year:
                month_time = month.total_duration()
                if month_time: 
                    time_list.append(month_time)
                    xlist.append(month.month[:3] + str(year.number)[-2:])
        
        ylist, labels, unit = self.finalize_time_labels(time_list)
        fig, ax = plt.subplots()
        graph = ax.bar(xlist, ylist)
        plt.bar_label(graph, labels=labels)
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Months')
        plt.ylabel(f'Time in {unit}')
        plt.title('Event Time Plot')
        plt.show()
        return fig

    def plot_time_date(self, year_num = None, month_name = None):
        time_list = []
        xlist = []
        if year_num: years = self.year_list.search_years(year_num)
        else: years = self.year_list
        for year in years:
            if month_name: months = year.search_months(month_name)
            else: months = year
            for month in months:
                for date in month:
                    date_time = date.total_duration()
                    if date_time:
                        time_list.append(date_time)
                        xlist.append(str(month_list.index(month.month.lower()) + 1) + '/' + str(date.date_num) + '/' + str(year.number)[-2:])
        
        ylist, labels, unit = self.finalize_time_labels(time_list)
        fig, ax = plt.subplots()
        graph = ax.bar(xlist, ylist)
        plt.bar_label(graph, labels=xlist, label_type='center', rotation=90, color='white')
        plt.bar_label(graph, labels=labels, rotation=90)
        plt.xticks([])
        plt.ylim(0,max(ylist) * 1.2)
        plt.xlabel('Dates')
        plt.ylabel(f'Time in {unit}')
        plt.title('Event Time Plot')
        plt.show()
        return fig
    
