from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label, Static, Input, Select
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Center
from textual.screen import Screen
from textual import on
from DocHandler import DocFactory
from DBHandler import DBFactory
from DataFuncs import DateFuncs, InfoFuncs, StatFuncs, PlotFuncs

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
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Input(type="integer", max_length=4)
            ),
            HorizontalGroup(
                Label("Month: "),
                Input(type="text")
            ),
            HorizontalGroup(
                Label("Date: "),
                Input(type="integer", max_length=2)
            ),
            self.ExitButton()
        )
        yield Footer()

class AddEventScreen(DefaultScreen):

    def __init__(self):
        super().__init__()
        self.datefuncs = DateFuncs(self.app.handler)

    @on(Select.Changed, "#months")
    def edit_dates(self, event: Select.Changed) -> None:
        month_select = self.query_one("#months", Select)
        max_dates = self.datefuncs.getMaxDays(month_select.value)
        date_select = self.query_one("#dates", Select)
        date_select.set_options( [(str(date), date) for date in range(1, max_dates + 1)] )

    @on(Select.Changed, "#years")
    def find_day(self, event: Select.Changed) -> None:
        pass

    @on(Select.Changed, "#days")
    def find_dates(self, event: Select.Changed) -> None:
        year_select = self.query_one("#years", Select)
        month_select = self.query_one("#months", Select)
        if year_select.value == Select.NULL or month_select.value == Select.NULL or event.value == Select.NULL:
            return
        year = year_select.value
        month = month_select.value
        day = event.value
        filtered_dates = self.datefuncs.getListofDates(year, month, day)
        date_select = self.query_one('#dates', Select)
        date_select.set_options( [(str(date), date) for date in filtered_dates] )


    def compose(self) -> ComposeResult:
        mins = range(1,61)
        hours = range(1,11)
        yield Header()
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Select( [(str(year), year) for year in range(2024, 2076) ] , id="years")
            ),
            HorizontalGroup(
                Label("Month: "),
                Select([ (f'{month[0].upper()}{month[1:]}', month) for month in self.datefuncs.getFullListofMonths() ], id="months")
            ),
            HorizontalGroup(
                Label("Date: "),
                Select( [(date, date) for date in range(1,32)], id="dates")
            ),
            HorizontalGroup(
                Label("Day: "),
                Select( [(f'{day[0].upper()}{day[1:]}', day) for day in self.datefuncs.getFullListofDays() ], id="days")
            ),
            HorizontalGroup(
                Label("Event name: "),
                Input(type="text")
            ),
            HorizontalGroup(
                Label("Duration: "),
                Select((str(hour), hour) for hour in hours),
                Label("hours and"),
                Select((str(min), min) for min in mins),
                Label("mins")
            ),
            HorizontalGroup(
                Label("Time: "),
                Input(type="integer", max_length=2),
                Label(":"),
                Input(type="integer", max_length=2, value="00"),
                Select([("am", 1), ("pm", 2)])
            ),
            self.ExitButton()
        )
        yield Footer()

class EditEventScreen(DefaultScreen):

    def __init__(self):
        super().__init__()
        self.infofuncs = InfoFuncs(self.app.handler)

    @on(Select.Changed, ".time_input")
    def update_time(self, event: Select.Changed) -> None:
        year_select = self.query_one("#years", Select)
        month_select = self.query_one("months", Select)

        if year_select.value and month_select.value:
            year_pick = year_select.value
            month_pick = month_select.value
            new_dates = []
            dates_select = self.query_one("#dates", Select)
            dates_select.set_options( [(f"")] )
        elif year_select.value:
            new_months = self.infofuncs.getListofMonths(int(event.value))
            month_select.set_options( [(month, month) for month in new_months] )
        elif month_select.value:
            pass
        


    def compose(self) -> ComposeResult:
        mins = range(1,61)
        hours = range(1,11)
        yield Header()
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Select( [(str(year), str(year)) for year in self.infofuncs.getListofYears()], id="years", classes="time-input")
            ),
            HorizontalGroup(
                Label("Month: "),
                Select([
                    ("January", 1),
                    ("February", 2),
                    ("March", 3),
                    ("April", 4),
                    ("May", 5),
                    ("June", 6),
                    ("July", 7),
                    ("August", 8),
                    ("September", 9),
                    ("October", 10),
                    ("November", 11),
                    ("December", 12)
                ], id="months", classes="time-input")
            ),
            HorizontalGroup(
                Label("Date: "),
                Select([], id="dates")
            ),
            HorizontalGroup(
                Label("Event name: "),
                Input(type="text")
            ),
            HorizontalGroup(
                Label("Duration: "),
                Select((str(hour), str(hour)) for hour in hours),
                #Input(type="integer", max_length=2),
                Label("hours and"),
                Select((str(min), str(min)) for min in mins),
                #Input(type="integer", max_length=2),
                Label("mins")
            ),
            HorizontalGroup(
                Label("Time: "),
                Input(type="integer", max_length=2),
                Label(":"),
                Input(type="integer", max_length=2, value="00"),
                Select([("am", 1), ("pm", 2)])
            ),
            self.ExitButton()
        )
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