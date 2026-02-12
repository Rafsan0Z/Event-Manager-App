from abc import ABC, abstractmethod
from EventExceptions import test_month, is_day
from DBHandler import DBFactory
from dotenv import load_dotenv
import os
import click

def start():
    #Open a database connection here
    database = DBFactory()
    setattr(Screen, 'database', database)
    screen = MainScreen
    while screen:
        screen.clear_screen()
        screen = screen.main()
    #Close that database connection here

class Screen(ABC):

    @classmethod
    @abstractmethod
    def main(cls):
        pass

    @classmethod
    def clear_screen(cls):
        click.clear()


class MainScreen(Screen):

    @classmethod
    def print_options(cls):
        print("(1) View Events")
        print("(2) Edit Events [Under Construction]")
        print("(3) Add Events [Under Construction]")
        print("(4) Plot Events")
        print("(5) Info")
        print("(Q) Exit")
        print(" Anything else will refresh the screen ")
    
    @classmethod
    def process_options(cls, option):
        match option:
            case '1':
                return ViewEventsScreen
            case '2':
                return EditEventsScreen
            case '3':
                return AddEventsScreen
            case '4':
                return PlotEventsScreen
            case '5':
                return InfoScreen
            case 'q':
                return None
            case _:
                return cls


    @classmethod
    def main(cls):
        print("This is the main screen")
        cls.print_options()
        option = input("Input: ")
        return cls.process_options(option.lower().strip())

class ViewAllEventsScreen(Screen):

    @classmethod
    def main(cls):
        print("This is the class method for the view events screen")
        print("Enter value to view filtered events. Only press enter if not to filter by that value, leave all filters blank to view all events")
        cls.database.grab_events()
        back = input("Enter anything to return")
        return ViewEventsScreen     

class ViewEventsScreen(Screen):
    
    @classmethod
    def print_options(cls):
        print("(1) View Yesterdays Events")
        print("(2) View Todays Events")
        print("(3) View Tomorrows Events")
        print("(4) View All Events")
        print("(5) View Filtered Events")
        print("(b) Go Back to the Main Screen")
        print("Any other inputs will have no affect")

    @classmethod
    def process_output(cls, option):
        match option:
            case '1':
                return YesterdaysEventScreen
            case '2':
                return TodaysEventsScreen
            case '3':
                return TomorrowsEventsScreen
            case '4':
                return ViewAllEventsScreen
            case '5':
                return ViewFilteredEventsScreen
            case 'b':
                return MainScreen
            case _:
                return cls

    @classmethod
    def main(cls):
        print("Choose from the following options")
        cls.print_options()
        output = input("Input: ").lower().strip()
        return cls.process_output(output) 


class InfoScreen(Screen):

    @classmethod
    def main(cls):
        load_dotenv(override=True)
        max_year, max_year_count = cls.database.find_max_event_year()
        max_month, max_month_count = cls.database.find_max_event_month()
        max_date, max_date_count = cls.database.find_max_event_date()
        print("Name of the Document:", os.getenv('FILE_NAME'))
        print("Number of Years:", len(cls.database.year_list))
        print("Year with the most events: {year} with {events} events".format(
            year = max_year.number,
            events = max_year_count
        ))
        print("Number of Months:", cls.database.year_list.num_months())
        print("Month with the most events: {month} of {year} with {events} events".format(
            month = max_month.month,
            year = max_month.year_num,
            events = max_month_count
        ))
        print("Number of Days:", cls.database.year_list.num_days())
        print("Day with the most events: {day} the {date}, {month} of {year} with {events} events".format(
            date = max_date.date_num,
            day = max_date.day_name,
            month = max_date.month_name,
            year = max_date.year_num,
            events = max_date_count
        ))
        print("Number of Events:", cls.database.year_list.num_events())
        print("Total time of events:", cls.database.total_time())
        print("Last modified time:", os.getenv("LAST_MODIFIED"))
        print("Github page:", os.getenv("GITHUB_URL"))
        input("Press anything to return\n")
        return MainScreen

class YesterdaysEventScreen(Screen):
    
    @classmethod
    def main(cls):
        print("Displaying Yesterdays Events:")
        cls.database.yesterdays_events()
        input("Press anything to return\n")
        return ViewEventsScreen


class TodaysEventsScreen(Screen):
    
    @classmethod
    def main(cls):
        print("Displaying Todays Events:")
        cls.database.todays_events()
        input("Press anything to return\n")
        return ViewEventsScreen


class TomorrowsEventsScreen(Screen):
    
    @classmethod
    def main(cls):
        print("Displaying Tomorrows Events: ")
        cls.database.tomorrows_events()
        input("Press anything to return\n")
        return ViewEventsScreen

class ViewFilteredEventsScreen(Screen):
    
    @classmethod
    def filter_message(cls, **options):
        result = "Displaying events based on: "
        if options.get('year', None):
            result += 'the Year ' + options.get('year') + "| "
        else: result += 'Any Year| '
        if options.get('month', None):
            result += 'the month of ' + options.get('month') + "| "
        else: result += 'Any Month| '
        if options.get('day', None):
            result += 'On ' + options.get('day') + "|"
        else: result += "Any Day|"
        if options.get('date', None):
            result += 'On ' + options.get('date') + "|"
        else: result += "Any Date|"
        print(result)

    @classmethod
    def process_time_item(cls, time_unit, test_func = None):
        output = input(time_unit + ": ").lower().strip()
        correct_input = False
        while test_func and output != '' and not correct_input:
            try:
                test_func(output)
            except Exception as e:
                output = input("Input a correct " + time_unit + " or leave it blank!! " + time_unit + ": ").lower().strip()
            else:
                correct_input = True
        return output if output else None

    @classmethod
    def main(cls):
        print("Enter the filter values, leave a filter empty if you want all events under that fileter")
        year = cls.process_time_item("Year")
        month = cls.process_time_item('Month', test_month)
        day = cls.process_time_item('Day', is_day)
        date = cls.process_time_item('Date')
        cls.filter_message(year=year,month=month,day=day,date=date)
        if year: year = int(year)
        if date: date = int(date)
        cls.database.grab_events(year,month,day,date)
        input("Press something to return: ")
        return ViewEventsScreen

class AddEventsScreen(Screen):
    
    @classmethod
    def main(cls):
        final = ''

        while final == '' or final == 'r':
            cls.clear_screen()
            event_name = input("First enter your Event name: ").strip()
            time = input("Now enter when this event will take place: ").strip().lower()
            day_name = input("Now enter the day name in full: ").strip()
            date_num = input("Now enter the date (numbers only): ").strip()
            month_name = input("Now enter the month name in full: ").strip()
            year_num = input("Finally, enter the year (numbers only): ").strip()

            print("You have entered an event with the following details: ")
            print("Event Name: {event}".format(event=event_name))
            print("Time: {time} on {day} the {date}, {month} {year}".format(
                time = time,
                day = day_name,
                date = date_num,
                month = month_name,
                year = year_num
            ))

            final = input("If these details are correct press F to continue. Otherwise Press R to start again: ").lower().strip()
        
        input("Your event has been added! Press anything to return\n")
        return MainScreen


class PlotEventsScreen(Screen):
    
    @classmethod
    def print_options(cls):
        print("Choose one of the following optipns:")
        print("(1) Plot Events by Year")
        print("(2) Plot Events by Month")
        print("(3) Plot Events by Date")
        print("(4) Plot Events by Time")
        print("(b) Back to Main Screen")
        print("Anything else will refresh the screen")

    @classmethod
    def process_output(cls):
        output = input('Enter a choice: ').strip().lower()
        match output:
            case '1':
                return PlotEventsByYearScreen
            case '2':
                return PlotEventsByMonthScreen
            case '3':
                return PlotEventsByDateScreen
            case '4':
                return PlotEventsTime
            case 'b':
                return MainScreen
            case _:
                return PlotEventsScreen


    @classmethod
    def main(cls):
        cls.print_options()
        return cls.process_output()

class GenericPlotScreen(Screen):

    @classmethod
    def save_plot(cls, plt):
        save_choice = input("If you want to save that graph, press S. Press anything else to not: ").lower()
        if save_choice == 's':
            file_name = input("Name the file or leave it empty for default file name (do not include any file extensions): ")
            if file_name.strip() == '':
                if cls == PlotEventsByAllDateScreen:
                    file_name = 'Plot_By_All_Date'
                elif cls == PlotEventsByYearDateScreen:
                    file_name = 'Plot_By_Yearly_Date'
                elif cls == PlotEventsByYearAndMonthDateScreen:
                    file_name = 'Plot_By_Yearly_and_Monthly_Date'
                elif cls == PlotEventsByMonthScreen:
                    file_name = 'Plot_By_Month'
                elif cls == PlotEventsByYearScreen:
                    file_name = 'Plot_By_Year'
                else: file_name = 'Defective'
            file_name += '.png'
            plt.savefig(file_name, dpi=300, bbox_inches='tight')

class PlotEventsTime(GenericPlotScreen):

    @classmethod
    def main(cls):
        print("Choose one of the following options")
        print("(1) Plot Time by Year")
        print("(2) Plot Time by Month")
        print("(3) Plot All Time")
    
class PlotEventsTimeByYear(GenericPlotScreen):

    @classmethod
    def main(cls):
        plt = cls.database.plot_events_time_by_year()
        cls.save_plot(plt)
        input("Press anything to go back\n")
        return PlotEventsTime

class PlotEventsTimeByMonth(GenericPlotScreen):

    @classmethod
    def main(cls):
        plt = cls.database.plot_events_time_by_month()
        cls.save_plot(plt)
        input("Press anything to go back\n")
        return PlotEventsTime

class PlotEventsTimeByDate(GenericPlotScreen):

    @classmethod
    def main(cls):
        input("Press anything to go back\n")
        return PlotEventsTime

class PlotEventsByMonthScreen(GenericPlotScreen):
    
    @classmethod
    def main(cls):
        plt = cls.database.plot_events_month()
        cls.save_plot(plt)
        input("Press anything to go back\n")
        return PlotEventsScreen

class PlotEventsByYearDateScreen(GenericPlotScreen):
    
    @classmethod
    def main(cls):
        year_num = input("Enter a year: ").lower().strip()
        while not year_num.isdigit():
            year_num = input("Please enter a proper year value: ")
        #plt = cls.database.plot_events_dates_by_year(int(year_num))
        plt = cls.database.plot_events_by_date('year', int(year_num))
        cls.save_plot(plt)
        return PlotEventsByDateScreen

class PlotEventsByYearAndMonthDateScreen(GenericPlotScreen):
    
    @classmethod
    def main(cls):
        year_num = input("Enter a year: ").lower().strip()
        while not year_num.isdigit():
            year_num = input("Please enter a proper year value: ").lower().strip()
        month_name = input("Enter a month: ").lower().strip()
        #plt = cls.database.plot_events_dates_by_year_and_month(int(year_num), month_name)
        plt = cls.database.plot_events_by_date('year month', int(year_num), month_name)
        cls.save_plot(plt)
        return PlotEventsByDateScreen

class PlotEventsByAllDateScreen(GenericPlotScreen):

    @classmethod
    def main(cls):
        plt = cls.database.plot_events_by_date('all')
        cls.save_plot(plt)
        input("Press anything to go back\n")
        return PlotEventsByDateScreen

class PlotEventsByDateScreen(GenericPlotScreen):

    @classmethod
    def print_choices(cls):
        print("Choose one of the following options: ")
        print("(1) Plot events by dates of a certain Year")
        print("(2) Plot events by dates of a certain Year AND Month")
        print("(3) Plot events by all dates")
        print("(b) Go back")
        print("Anything else will refresh the screen")

    @classmethod
    def process_output(cls):
        choice = input("Enter a choice: ").lower().strip()
        match choice:
            case '1':
                return PlotEventsByYearDateScreen
            case '2':
                return PlotEventsByYearAndMonthDateScreen
            case '3':
                return PlotEventsByAllDateScreen
            case 'b':
                return PlotEventsScreen
            case _:
                return cls

    @classmethod
    def main(cls):
        cls.print_choices()
        return cls.process_output()

class PlotEventsByYearScreen(GenericPlotScreen):

    @classmethod
    def main(cls):
        plt = cls.database.plot_events_year()
        cls.save_plot(plt)
        input("Press anything to go back")
        return PlotEventsScreen

class EditEventsScreen(Screen):

    @classmethod
    def filter_message(cls, **options):
        result = "Displaying events based on: "
        if options.get('year', None):
            result += 'the Year ' + options.get('year') + "| "
        else: result += 'Any Year| '
        if options.get('month', None):
            result += 'the month of ' + options.get('month') + "| "
        else: result += 'Any Month| '
        if options.get('day', None):
            result += 'On ' + options.get('day') + "|"
        else: result += "Any Day|"
        print(result)
    
    @classmethod
    def process_time_item(cls, time_unit, test_func = None):
        output = input(time_unit + ": ").lower().strip()
        correct_input = False
        while test_func and output != '' and not correct_input:
            try:
                test_func(output)
            except Exception as e:
                output = input("Input a correct " + time_unit + " or leave it blank!! " + time_unit + ": ").lower().strip()
            else:
                correct_input = True
        return output


    @classmethod
    def main(cls):
        choice = ''

        while choice == '' or choice == 'r':
            print("We'll edit the chosen event here, only one event can be edited at a time [for now!]")
            print("Enter the filter values, leave a filter empty if you want all events under that fileter")
            year = cls.process_time_item("Year")
            month = cls.process_time_item('Month', test_month)
            day = cls.process_time_item('Day', is_day)
            cls.filter_message(year=year,month=month,day=day)

            choice = input("Now pick one of the following events by entering the number. Enter B to go back to the Main Screen. Enter anything else to reset your filters: ").lower().strip()
            if choice == 'b': return MainScreen
            elif choice.isdigit(): break
            else : cls.clear_screen()
        
        input("Edit complete! Press anything to go back: ")
        return MainScreen


class UpcomingEventsScreen(Screen):

    @classmethod
    def main(cls):
        pass

#screens = [MainScreen, ViewEventsScreen]
# for screen in screens:
#     screen.main()

#start()