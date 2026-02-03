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
    def main(cls):
        print("This is the main screen")
        print("(1) View All Events")
        print("(Q) Exit")
        print(" Anything else will refresh the screen ")
        option = input("Input: ")
        if option.lower().strip() == '1':
            return ViewEventsScreen
        elif option.lower().strip() == 'q':
            return None
        else:
            return cls


class ViewEventsScreen(Screen):

    @classmethod
    def main(cls):
        print("This is the class method for the view events screen")
        print("Now enter anything to go back")
        output = input("Input: ")
        return MainScreen

#screens = [MainScreen, ViewEventsScreen]
# for screen in screens:
#     screen.main()

screen = MainScreen
while(screen):
    #print(screen)
    screen.clear_screen()
    screen = screen.main()