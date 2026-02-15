from abc import ABC, abstractmethod
from EventExceptions import test_month, is_day
from DBHandler import DBFactory
from DataFuncs import InfoFuncs, StatFuncs, PlotFuncs
from dotenv import load_dotenv
import os
import click

def start():
    database_handler = DBFactory()
    Screen.db_handler = database_handler
    screen = MainScreen()
    while screen:
        screen.clear_screen()
        screen = screen.main()

class Screen(ABC):

    @abstractmethod
    def main(cls):
        pass

    @staticmethod
    def clear_screen():
        click.clear()

class MainScreen(Screen):

    def print_options(self):
        print("(1) View Events")
        print("(2) Edit Events [Under Construction]")
        print("(3) Add Events [Under Construction]")
        print("(4) Plot Events")
        print("(5) Info")
        print("(Q) Exit")
        print(" Anything else will refresh the screen ")

    def process_inputs(self):
        option = input("Input: ")
        match option:
            case '1':
                return ViewEventsScreen()
            case '2':
                return EditEventsScreen()
            case '3':
                return AddEventsScreen()
            case '4':
                return PlotScreen()
            case '5':
                return InfoScreen()
            case 'q':
                return None
            case _:
                return self
            
    def main(self):
        print("This is the main screen")
        self.print_options()
        return self.process_inputs()

class ViewAllEventsScreen(Screen):

    def main(self):
        print("This is the class method for the view events screen")
        print("Enter value to view filtered events. Only press enter if not to filter by that value, leave all filters blank to view all events")
        self.db_handler.grab_events()
        input("Enter anything to return ")
        return ViewEventsScreen()

class ViewEventsScreen(Screen):

    def print_options(self):
        print("(1) View Yesterdays Events")
        print("(2) View Todays Events")
        print("(3) View Tomorrows Events")
        print("(4) View All Events")
        print("(5) View Filtered Events")
        print("(b) Go Back to the Main Screen")
        print("Any other inputs will have no affect")

    def process_input(self):
        option = input("Input: ").lower().strip()
        match option:
            case '1':
                return YesterdaysEventScreen()
            case '2':
                return TodaysEventScreen()
            case '3':
                return TomorrowsEventScreen()
            case '4':
                return ViewAllEventsScreen()
            case '5':
                return ViewFilteredEventsScreen()
            case 'b':
                return MainScreen()
            case _:
                return self

    def main(self):
        print("Choose from the following options")
        self.print_options()
        return self.process_input()

class InfoScreen(Screen):

    def main(self):
        infofuncs = InfoFuncs(self.db_handler)
        statfuncs = StatFuncs(self.db_handler)
        max_year, max_year_count = statfuncs.find_max_event_year()
        max_month, max_month_count = statfuncs.find_max_event_month()
        max_date, max_date_count = statfuncs.find_max_event_date()
        print("Name of the Document:", infofuncs.getDocName())
        print("Number of Years:", infofuncs.getNumofYears())
        print("Year with the most events: {year} with {events} events".format(
            year = max_year.number,
            events = max_year_count
        ))
        print("Number of Months:", infofuncs.getNumofMonths())
        print("Month with the most events: {month} of {year} with {events} events".format(
            month = max_month.month,
            year = max_month.year_num,
            events = max_month_count
        ))
        print("Number of Days:", infofuncs.getNumofDays())
        print("Day with the most events: {day} the {date}, {month} of {year} with {events} events".format(
            date = max_date.date_num,
            day = max_date.day_name,
            month = max_date.month_name,
            year = max_date.year_num,
            events = max_date_count
        ))
        print("Number of Events:", infofuncs.getNumofEvents())
        print("Total time of events:", statfuncs.total_time())
        print("Last modified time:", infofuncs.getLastModTime())
        print("Github page:", infofuncs.getGithubLink())
        input("Press anything to return\n")
        return MainScreen()

class YesterdaysEventScreen(Screen):

    def main(self):
        print("Displaying Yesterdays Events...")
        infofuncs = InfoFuncs(self.db_handler)
        infofuncs.getYesterdaysEvents()
        input("Press anything to return ")
        return ViewEventsScreen()

class TodaysEventScreen(Screen):

    def main(self):
        print("Displaying Todays Events...")
        infofuncs = InfoFuncs(self.db_handler)
        infofuncs.getTodaysEvents()
        input("Press anything to return ")
        return ViewEventsScreen()

class TomorrowsEventScreen(Screen):

    def main(self):
        print("Displaying Tomorrows Events: ")
        infofuncs = InfoFuncs(self.db_handler)
        infofuncs.getTomorrowsEvents()
        input("Press anything to return ")
        return ViewEventsScreen()

class ViewFilteredEventsScreen(Screen):

    def filter_message(self, **options):
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

    def process_time_item(self, time_unit, test_func = None):
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
    
    def main(self):
        print("Enter the filter values, leave a filter empty if you want all events under that fileter")
        year = self.process_time_item("Year")
        month = self.process_time_item('Month', test_month)
        day = self.process_time_item('Day', is_day)
        date = self.process_time_item('Date')
        self.filter_message(year=year,month=month,day=day,date=date)
        if year: year = int(year)
        if date: date = int(date)
        #cls.database.grab_events(year,month,day,date)
        input("Press something to return: ")
        return ViewEventsScreen()

class AddEventsScreen(Screen):

    def main(self):
        final = ''

        while final == '' or final == 'r':
            self.clear_screen()
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
        return MainScreen()


class EditEventsScreen(Screen):

    def filter_message(self, **options):
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
    
    def process_time_item(self, time_unit, test_func = None):
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

    def main(self):
        choice = ''

        while choice == '' or choice == 'r':
            print("We'll edit the chosen event here, only one event can be edited at a time [for now!]")
            print("Enter the filter values, leave a filter empty if you want all events under that fileter")
            year = self.process_time_item("Year")
            month = self.process_time_item('Month', test_month)
            day = self.process_time_item('Day', is_day)
            self.filter_message(year=year,month=month,day=day)

            choice = input("Now pick one of the following events by entering the number. Enter B to go back to the Main Screen. Enter anything else to reset your filters: ").lower().strip()
            if choice == 'b': return MainScreen()
            elif choice.isdigit(): break
            else : self.clear_screen()
        
        input("Edit complete! Press anything to go back: ")
        return MainScreen()

class PlotScreen(Screen):

    def print_options(self):
        print("Choose one of the following options: ")
        print("(1) Plot By Events")
        print("(2) Plot By Time")
        print("(b) Go back")
        print("Anything else will refresh the screen")

    def process_input(self):
        choice = input("Input: ").lower().strip()
        match choice:
            case '1':
                return PlotEventsScreen()
            case '2':
                return PlotTimeScreen()
            case 'b':
                return MainScreen()
            case _:
                return self
    
    def main(self):
        self.print_options()
        return self.process_input()


class PlotEventsScreen(Screen):

    def print_options(self):
        print("Choose one of the following optipns:")
        print("(1) Plot Events by Year")
        print("(2) Plot Events by Month")
        print("(3) Plot Events by Date")
        print("(b) Back to Main Screen")
        print("Anything else will refresh the screen")

    def process_output(self):
        output = input('Enter a choice: ').strip().lower()
        match output:
            case '1':
                return PlotEventsByYear()
            case '2':
                return PlotEventsByMonth()
            case '3':
                return PlotEventsByDate()
            case 'b':
                return MainScreen()
            case _:
                return self
            
    def main(self):
        self.print_options()
        return self.process_output()


class GenericPlotScreen(Screen):

    def save_plot(self, plt):
        save_choice = input("If you want to save that graph, press S. Press anything else to not: ").lower()
        if save_choice == 's':
            file_name = input("Name the file or leave it empty for default file name (do not include any file extensions): ")
            match self:
                case PlotEventsByDate():
                    file_name = 'Plot_By_Date'
                case PlotEventsByMonth():
                    file_name = 'Plot_By_Month'
                case PlotEventsByYear():
                    file_name = 'Plot_By_Year'
                case _:
                    file_name = 'defective'
            file_name += '.png'
            plt.savefig(file_name, dpi=300, bbox_inches='tight')


class PlotEventsByYear(GenericPlotScreen):

    def main(self):
        plotfuncs = PlotFuncs(self.db_handler)
        plt = plotfuncs.plot_events_year()
        #plt = cls.database.plot_events_year()
        self.save_plot(plt)
        input("Press anything to go back")
        return PlotEventsScreen()

class PlotEventsByMonth(Screen):
    
    class ByYear(GenericPlotScreen):

        def process_input(self):
            year_num = input("Enter a year: ").lower().strip()
            while not year_num.isdigit() and year_num != 'b':
                year_num = input("Please enter a valid year, or B to go back: ")
            return year_num


        def main(self):
            year_num = self.process_input()
            if year_num == 'b': return PlotEventsByMonth()
            plt = PlotFuncs(self.db_handler).plot_events_month(int(year_num))
            self.save_plot(plt)
            input("Press anything to go back")
            return PlotEventsByMonth()

    class AllMonths(GenericPlotScreen):
        
        def main(self):
            plt = PlotFuncs(self.db_handler).plot_events_month()
            self.save_plot(plt)
            input("Press anything to go back")
            return PlotEventsByMonth()


    def print_options(self):
        print("Choose one of the following ")
        print("(1) Plot events by months of a certain year")
        print("(2) Plot events by all months")
        print("(b) Go Back")
        print("Anything else will refresh the screen ")

    def process_input(self):
        choice = input("Input: ").lower().strip()
        match choice:
            case '1':
                return PlotEventsByMonth.ByYear()
            case '2':
                return PlotEventsByMonth.AllMonths()
            case 'b':
                return PlotEventsScreen()
            case _:
                return self

    def main(self):
        self.print_options()
        return self.process_input()
        

class PlotEventsByDate(Screen):

    class ByYear(GenericPlotScreen):
        
        def main(self):
            year_num = input("Enter a year: ").lower().strip()
            while not year_num.isdigit():
                year_num = input("Please enter a proper year value: ").lower().strip()
            plt = PlotFuncs(self.db_handler).plot_events_date(int(year_num))
            self.save_plot(plt)
            return PlotEventsByDate()

    class ByMonthandYear(GenericPlotScreen):
        
        def main(self):
            year_num = input("Enter a year: ").lower().strip()
            while not year_num.isdigit():
                year_num = input("Please enter a proper year value: ").lower().strip()
            month_name = input("Enter a month: ").lower().strip()
            plt = PlotFuncs(self.db_handler).plot_events_date(int(year_num), month_name)
            self.save_plot(plt)
            return PlotEventsByDate()


    class AllDates(GenericPlotScreen):
        
        def main(self):
            plt = PlotFuncs(self.db_handler).plot_events_date()
            self.save_plot(plt)
            input("Press anything to go back\n")
            return PlotEventsByDate()

    def print_choices(self):
        print("Choose one of the following options: ")
        print("(1) Plot events by dates of a certain Year")
        print("(2) Plot events by dates of a certain Year AND Month")
        print("(3) Plot events by all dates")
        print("(b) Go back")
        print("Anything else will refresh the screen")

    def process_input(self):
        choice = input("Enter a choice: ").lower().strip()
        match choice:
            case '1':
                return PlotEventsByDate.ByYear()
            case '2':
                return PlotEventsByDate.ByMonthandYear()
            case '3':
                return PlotEventsByDate.AllDates()
            case 'b':
                return PlotEventsScreen()
            case _:
                return self

    def main(self):
        self.print_choices()
        return self.process_input()


class PlotTimeScreen(Screen):

    def print_options(self):
        print("Choose one of the following options")
        print("(1) Plot Time by Year")
        print("(2) Plot Time by Month")
        print("(3) Plot Time by Date")
        print("(b) Go Back")
        print("Anything else will refresh the screen")

    def process_input(self):
        choice = input("Input: ").lower().strip()
        match choice:
            case '1':
                return PlotTimeByYear()
            case '2':
                return PlotTimeByMonth()
            case '3':
                return PlotTimeByDate()
            case 'b':
                return PlotScreen()
            case _:
                return self
    
    def main(self):
        self.print_options()
        return self.process_input()

class PlotTimeByYear(GenericPlotScreen):

    def main(self):
        plt = PlotFuncs(self.db_handler).plot_time_year()
        self.save_plot(plt)
        input("Press anything to go back\n")
        return PlotTimeScreen()

class PlotTimeByMonth(Screen):

    class ByYear(GenericPlotScreen):
        
        def main(self):
            year_num = input("Enter a year: ").lower().strip()
            while not year_num.isdigit():
                year_num = input("Please enter a proper year value: ").lower().strip()
            plt = PlotFuncs(self.db_handler).plot_time_month(int(year_num))
            self.save_plot(plt)
            input("Press anything to go back\n")
            return PlotTimeScreen()

    class AllMonths(GenericPlotScreen):
        
        def main(self):
            plt = PlotFuncs(self.db_handler).plot_time_month()
            self.save_plot(plt)
            input("Press anything to go back\n")
            return PlotTimeScreen()

    def print_options(self):
        print("Choose one of the following ")
        print("(1) Plot Time by months of a certain year")
        print("(2) Plot Time by all months")
        print("(b) Go Back")
        print("Anything else will refresh the screen")

    def process_input(self):
        choice = input("Input: ").lower().strip()
        match choice:
            case '1':
                return PlotTimeByMonth.ByYear()
            case '2':
                return PlotTimeByMonth.AllMonths()
            case 'b':
                return PlotTimeScreen()
            case _:
                return self
    
    def main(self):
        self.print_options()
        return self.process_input()

class PlotTimeByDate(Screen):

    class ByYear(GenericPlotScreen):
        
        def main(self):
            year_num = input("Enter a year: ").lower().strip()
            while not year_num.isdigit():
                year_num = input("Please enter a proper year value: ").lower().strip()
            plt = PlotFuncs(self.db_handler).plot_time_date(int(year_num))
            input("Press anything to go back\n")
            return PlotTimeScreen()

    class ByMonthandYear(GenericPlotScreen):
        
        def main(self):
            input("Press anything to go back\n")
            return PlotTimeScreen()

    class AllDates(GenericPlotScreen):
        
        def main(self):
            plt = PlotFuncs(self.db_handler).plot_time_date()
            input("Press anything to go back\n")
            return PlotTimeScreen()

    def print_options(self):
        print("Choose one of the following ")
        print("(1) Plot Time by dates of a certain year")
        print("(2) Plot Time by dates of a certain year and month")
        print("(3) Plot Time by all dates")
        print("(b) Go Back")
        print("Anything else will refresh the screen")

    def process_input(self):
        choice = input("Input: ").lower().strip()
        match choice:
            case '1':
                return PlotTimeByDate.ByYear()
            case '2':
                return PlotTimeByDate.ByMonthandYear()
            case '3':
                return PlotTimeByDate.AllDates()
            case 'b':
                return PlotTimeScreen()
            case _:
                return self
    
    def main(self):
        self.print_options()
        return self.process_input()
