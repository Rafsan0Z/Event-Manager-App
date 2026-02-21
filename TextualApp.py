from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits, Static
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Center
from textual.screen import Screen
from textual import on

class DefaultScreen(Screen):

    @on(Button.Pressed, "#back")
    def back(self):
        self.app.pop_screen()

    def ExitButton(self):
        return Button("Back", id="back", variant="error")

    

class MainScreen(Screen):

    @on(Button.Pressed, "#exit-btn")
    def exit_app(self):
        self.app.exit()

    @on(Button.Pressed, "#view_events")
    def view_screen(self):
        self.app.push_screen("view")

    @on(Button.Pressed, "#add_events")
    def add_screen(self):
        self.app.push_screen("add")

    @on(Button.Pressed, "#edit_events")
    def edit_screen(self):
        self.app.push_screen("edit")

    @on(Button.Pressed, "#plot_events")
    def plot_screen(self):
        self.app.push_screen("plot")

    @on(Button.Pressed, "#info")
    def info_screen(self):
        self.app.push_screen("info")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("View Events", id="view_events")
        yield Button("Add Events", id="add_events")
        yield Button("Edit Events", id="edit_events")
        yield Button("Plot Events", id="plot_events")
        yield Button("Info", id="info")
        yield Button("Exit", id="exit-btn", variant="error")
        yield Footer()

class ViewEventScreen(DefaultScreen):
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield self.ExitButton()
        yield Footer()

class AddEventScreen(DefaultScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.ExitButton()
        yield Footer()

class EditEventScreen(DefaultScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.ExitButton()
        yield Footer()

class PlotEventScreen(DefaultScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.ExitButton()
        yield Footer()

class InfoScreen(DefaultScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Name of the document: ")
        yield Static("Number of Years: ")
        yield Static("Year with the most events: ")
        yield Static("Number of Months: ")
        yield Static("Month with the most events: ")
        yield Static("Number of Days: ")
        yield Static("Days with the most events: ")
        yield Static("Number of Events: ")
        yield Static("Total time of events: ")
        yield Static("Last modified time: ")
        yield Static("Github Page: ")
        yield self.ExitButton()
        yield Footer()

class TestApp(App):

    CSS_PATH = "test.tcss"
    LIGHT_MODE = 'textual-light'
    DARK_MODE = 'textual-dark'
    BINDINGS = [('d', 'dark_toggle', 'Toggle Dark Mode!')
    ]

    SCREENS = {
        "main": MainScreen,
        "view": ViewEventScreen,
        "add": AddEventScreen,
        "edit": EditEventScreen,
        "plot": PlotEventScreen,
        "info": InfoScreen
    }

    def on_mount(self):
        self.push_screen("main")

    def action_dark_toggle(self) -> None:
        self.theme = (
            self.DARK_MODE if self.theme == 'textual-light' else self.LIGHT_MODE
        )
    
TestApp().run()