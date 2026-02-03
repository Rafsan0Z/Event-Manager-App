from abc import ABC, abstractmethod
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
        print("(1) View All Events")
        print("(2) Edit Events")
        print("(Q) Exit")
        print(" Anything else will refresh the screen ")
    
    @classmethod
    def process_options(cls, option):
        match option:
            case '1':
                return ViewEventsScreen
            case '2':
                return EditEventsScreen
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

class ViewEventsScreen(Screen):

    @classmethod
    def main(cls):
        print("This is the class method for the view events screen")
        print("Enter value to view filtered events. Only press enter if not to filter by that value, leave all filters blank to view all events")
        year = input("Year: ")
        month = input("Month: ")
        day = input("Day: ")
        return MainScreen
    
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
    def main(cls):
        print("We'll edit the chosen event here, only one event can be edited at a time [for now!]")
        print("Enter the filter values, leave a filter empty if you want all events under that fileter")
        year = input("Year: ")
        month = input("Month: ")
        day = input("Day: ")
        cls.filter_message(year=year,month=month,day=day)


#screens = [MainScreen, ViewEventsScreen]
# for screen in screens:
#     screen.main()

screen = MainScreen
while(screen):
    #print(screen)
    screen.clear_screen()
    screen = screen.main()