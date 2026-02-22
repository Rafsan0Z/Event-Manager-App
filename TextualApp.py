from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label, Static, Input
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Center
from textual.screen import Screen
from textual import on
from DocHandler import DocFactory
from DBHandler import DBFactory
from DataFuncs import InfoFuncs, StatFuncs, PlotFuncs

class DefaultScreen(Screen):

    def __init__(self):
        super().__init__()
        if len(self.app.screen_stack) > 1:
            self.parent_screen = self.app.screen_stack[-1]
        else:
            self.parent_screen = None

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

class PlotScreen(DefaultScreen):

    @on(Button.Pressed, "#event_plot")
    def plot_events(self):
        self.app.push_screen(PlotEventScreen())

    @on(Button.Pressed, "#time_plot")
    def plot_time(self):
        self.app.push_screen(PlotTimeScreen())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Plot by Events", id="event_plot")
        yield Button("Plot by Time", id="time_plot")
        yield self.ExitButton()
        yield Footer()

class PlotEventScreen(DefaultScreen):

    @on(Button.Pressed, "#by_year")
    def plot_screen_by_year(self):
        self.app.push_screen(ByYear())

    @on(Button.Pressed, "#by_month")
    def plot_screen_by_month(self):
        self.app.push_screen(ByMonth())

    @on(Button.Pressed, "#by_date")
    def plot_screen_by_date(self):
        self.app.push_screen(ByDate())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Plot Events By Year", id="by_year")
        yield Button("Plot Events By Month", id="by_month")
        yield Button("Plot Events By Date", id="by_date")
        yield self.ExitButton()
        yield Footer()

class PlotTimeScreen(DefaultScreen):

    @on(Button.Pressed, "#by_year")
    def plot_screen_by_year(self):
        self.app.push_screen(ByYear())

    @on(Button.Pressed, "#by_month")
    def plot_screen_by_month(self):
        self.app.push_screen(ByMonth())

    @on(Button.Pressed, "#by_date")
    def plot_screen_by_date(self):
        self.app.push_screen(ByDate())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Plot Time By Year", id="by_year")
        yield Button("Plot Time By Month", id="by_month")
        yield Button("Plot Time By Date", id="by_date")
        yield self.ExitButton()
        yield Footer()


class ByYear(DefaultScreen):

    def __init__(self):
        super().__init__()
        if isinstance(self.parent_screen, PlotEventScreen):
            self.plot_func = PlotFuncs(self.app.handler).plot_events_year
        elif isinstance(self.parent_screen, PlotTimeScreen):
            self.plot_func = PlotFuncs(self.app.handler).plot_time_year

    @on(Button.Pressed, "#show")
    def show_plot(self):
        plt, self.fig = self.plot_func()
        plt.show()
    
    @on(Button.Pressed, "#save")
    def save_plot(self):
        if not self.fig:
            self.fig = self.plot_func()[-1]
        # save it here

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Button(f"Show Plot", id="show"),
            Button("Save Plot", id="save"),
            self.ExitButton()
        )
        yield Footer()

class ByMonth(DefaultScreen):

    def __init__(self):
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Input(type="integer", max_length=4)
            ),
            Button("Show Plot"),
            Button("Save Plot"),
            self.ExitButton()
        )
        yield Footer()

class ByDate(DefaultScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Input(type="integer", max_length=4)
            ),
            HorizontalGroup(
                Label("Month: "),
                Input(type="text")
            ),
            Button("Show Plot"),
            Button("Save Plot"),
            self.ExitButton()
        )
        yield Footer()

class InfoScreen(DefaultScreen):

    def __init__(self):
        super().__init__()
        self.infofuncs = InfoFuncs(self.app.handler)
        self.statfuncs = StatFuncs(self.app.handler)

    def compose(self) -> ComposeResult:
        max_year, max_year_count = self.statfuncs.find_max_event_year()
        max_month, max_month_count = self.statfuncs.find_max_event_month()
        max_date, max_date_count = self.statfuncs.find_max_event_date()
        yield Header()
        yield VerticalScroll(
            Static(f"Name of the document: {self.infofuncs.getDocName()}"),
            Static(f"Number of Years: {self.infofuncs.getNumofYears()}"),
            Static(f"Year with the most events: {max_year.number} with {max_year_count} events"),
            Static(f"Number of Months: {self.infofuncs.getNumofMonths()}"),
            Static(f"Month with the most events: {max_month.month} of {max_month.year_num} with {max_month_count} events"),
            Static(f"Number of Days: {self.infofuncs.getNumofDays()}"),
            Static(f"Days with the most events: {max_date.day_name} the {max_date.date_num}, {max_date.month_name} of {max_date.year_num} with {max_date_count} events"),
            Static(f"Number of Events: {self.infofuncs.getNumofEvents()}"),
            Static(f"Total time of events: {self.statfuncs.total_time()}"),
            Static(f"Last modified time: {self.infofuncs.getLastModTime()}"),
            Static(f"Github Page: {self.infofuncs.getGithubLink()}"),
            self.ExitButton()
        )
        yield Footer()

class EventManager(App):

    def __init__(self):
        super().__init__()
        DocFactory()
        self.handler = DBFactory()


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
        "plot": PlotScreen,
        "info": InfoScreen
    }

    def on_mount(self):
        self.push_screen("main")

    def action_dark_toggle(self) -> None:
        self.theme = (
            self.DARK_MODE if self.theme == 'textual-light' else self.LIGHT_MODE
        )
    
EventManager().run()