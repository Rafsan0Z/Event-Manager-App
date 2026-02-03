from abc import ABC, abstractmethod

class Screen(ABC):

    @classmethod
    @abstractmethod
    def main(cls):
        pass


class MainScreen(Screen):

    @classmethod
    def main(cls):
        print("This is a class method")
        return ViewEventsScreen


class ViewEventsScreen(Screen):

    @classmethod
    def main(cls):
        print("This is the class method for the view events screen")

screens = [MainScreen, ViewEventsScreen]
for screen in screens:
    screen.main()

screen = MainScreen
while(screen):
    print(screen)
    screen = screen.main()