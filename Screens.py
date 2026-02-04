from abc import ABC, abstractmethod
from EventExceptions import test_month, is_day, BadMonthException
import click

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
        print("(2) Edit Events")
        print("(3) Add Events")
        print("(4) Plot Events")
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
        year = input("Year: ")
        month = input("Month: ")
        day = input("Day: ")
        return MainScreen

class ViewEventsScreen(Screen):
    
    @classmethod
    def print_options(cls):
        print("(1) View Yesterdays Events")
        print("(2) View Todays Events")
        print("(3) View Tomorrows Events")
        print("(4) View All Events")
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


class YesterdaysEventScreen(Screen):
    
    @classmethod
    def main(cls):
        print("Displaying Yesterdays Events:")


class TodaysEventsScreen(Screen):
    
    @classmethod
    def main(cls):
        print("Displaying Todays Events:")


class TomorrowsEventsScreen(Screen):
    pass

class AddEventsScreen(Screen):
    pass

class PlotEventsScreen(Screen):
    pass
    
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
        print("We'll edit the chosen event here, only one event can be edited at a time [for now!]")
        print("Enter the filter values, leave a filter empty if you want all events under that fileter")
        year = cls.process_time_item("Year")
        month = cls.process_time_item('Month', test_month)
        day = cls.process_time_item('Day', is_day)
        cls.filter_message(year=year,month=month,day=day)


class UpcomingEventsScreen(Screen):

    @classmethod
    def main(cls):
        pass

#screens = [MainScreen, ViewEventsScreen]
# for screen in screens:
#     screen.main()

def start():
    #Open a database connection here
    screen = MainScreen
    while screen:
        screen.clear_screen()
        screen = screen.main()
    #Close that database connection here

start()