from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label, Static, Input, Select
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Center, Container
from textual.screen import Screen
from textual import on
from DocHandler import DocFactory
from DBHandler import DBFactory
from Changes import ChangeList
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
        self.app.push_screen(ViewEventScreen())

    @on(Button.Pressed, "#add_events")
    def add_screen(self):
        self.app.push_screen(AddEventScreen())

    @on(Button.Pressed, "#edit_events")
    def edit_screen(self):
        self.app.push_screen(EditEventScreen())

    @on(Button.Pressed, "#plot_events")
    def plot_screen(self):
        self.app.push_screen(PlotEventScreen())

    @on(Button.Pressed, "#info")
    def info_screen(self):
        self.app.push_screen(InfoScreen())

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

    def find_missing_inputs(self, main_scroll: VerticalScroll) -> list:
        not_entered = []
        year = main_scroll.query_one("#years", Select).value
        if year == Select.NULL: not_entered.append("Year")
        month = main_scroll.query_one("#months", Select).value
        if month == Select.NULL: not_entered.append("Month")
        date = main_scroll.query_one("#dates", Select).value
        if date == Select.NULL: not_entered.append("Date")
        day = main_scroll.query_one("#days", Select).value
        if day == Select.NULL: not_entered.append("Day Name")

        event_name = main_scroll.query_one("#event_name", Input).value
        if not event_name: not_entered.append("Event name")
        hour_duration = main_scroll.query_one("#hours_duration", Select).value
        min_duration = main_scroll.query_one("#mins_duration", Select).value
        if hour_duration == Select.NULL or min_duration == Select.NULL: not_entered.append("Completed duration info")
        hour_time = main_scroll.query_one("#hours_time", Select).value
        min_time = main_scroll.query_one("#mins_time", Select).value
        period_time = main_scroll.query_one("#am_pm", Select).value
        if hour_time == Select.NULL or min_time == Select.NULL or period_time == Select.NULL: not_entered.append("Completed time info")
        return not_entered

    @on(Select.Changed, ".times")
    def update_times(self):
        year_select = self.query_one("#years", Select)
        month_select = self.query_one("#months", Select)
        date_select = self.query_one("#dates", Select)
        day_select = self.query_one("#days", Select)
        year = year_select.value
        month = month_select.value
        day = day_select.value
        date = date_select.value

        if year != Select.NULL and month != Select.NULL and date != Select.NULL and day != Select.NULL:
            return
        if year != Select.NULL and month != Select.NULL and date != Select.NULL:
            only_day = self.datefuncs.getDay(year, month, date)
            day_select.set_options( [(only_day, only_day)] )
            return
        if year != Select.NULL and month != Select.NULL:
            if day != Select.NULL:
                filtered_dates = self.datefuncs.getListofDates(year, month, day)
                date_select.set_options( [(str(date), date) for date in filtered_dates] )
                return 
        if month != Select.NULL:
            max_dates = self.datefuncs.getMaxDays(month_select.value)
            date_select.set_options( [(str(date), date) for date in range(1, max_dates + 1)] )

    @on(Button.Pressed, '#enter')
    async def enter(self) -> None:
        main_scroll = self.query_one("#main", VerticalScroll)
        for label in main_scroll.query(".errors"): await label.remove()
        if main_scroll.query_one_optional("#error_label"): await main_scroll.query_one_optional("#error_label").remove()

        not_entered = self.find_missing_inputs(main_scroll)
        
        if len(not_entered):

            label_list = [Label(entry, classes="errors", variant="error") for entry in not_entered]
            
            main_scroll.mount(
                Label(f"You're missing the following: ", id="error_label"),
                *label_list,
            )
        else:
            #self.app.changeList.add_event_change()
            pass

    def compose(self) -> ComposeResult:
        mins = range(61)
        hours = range(1,11)
        times = range(1,13)
        yield Header()
        yield VerticalScroll(
            HorizontalGroup(
                Label("Year: "),
                Select( [
                    (f'{year}', year) for year in range(2024, 2076) 
                ] , id="years", classes="times")
            ),
            HorizontalGroup(
                Label("Month: "),
                Select([ 
                    (f'{month[0].upper()}{month[1:]}', month) for month in self.datefuncs.getFullListofMonths() 
                ], id="months", classes="times")
            ),
            HorizontalGroup(
                Label("Date: "),
                Select( [
                    (date, date) for date in range(1,32)
                ], id="dates", classes="times")
            ),
            HorizontalGroup(
                Label("Day: "),
                Select( [
                    (f'{day[0].upper()}{day[1:]}', day) for day in self.datefuncs.getFullListofDays() 
                ], id="days", classes='times')
            ),
            HorizontalGroup(
                Label("Event name: "),
                Input(type="text", id="event_name")
            ),
            HorizontalGroup(
                Label("Duration: "),
                Select( [
                    (f'{hour}', hour) for hour in hours
                ], id="hours_duration", value=1),
                Label("hours and"),
                Select( [
                    (f'{min}', min) for min in mins
                ], id="mins_duration", value=0),
                Label("mins")
            ),
            HorizontalGroup(
                Label("Time: "),
                Select([
                    (f'0{time}', time) if time < 10 else (f'{time}', time) for time in times
                ], id="hours_time", value=12),
                Label(":"),
                Select( [
                    (f'0{min}', min) if min < 10 else (f'{min}', min) for min in mins[:-1]
                ], id="mins_time", value=0),
                Select([("AM", "am"), ("PM", "pm")], id="am_pm", value="pm")
            ),
            Button("Enter", id="enter"),
            self.ExitButton(),
            id="main"
        )
        yield Footer()

class EditEventScreen(DefaultScreen):

    def __init__(self):
        super().__init__()
        self.datefuncs = DateFuncs(self.app.handler)

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
            new_months = self.datefuncs.getListofMonths(int(event.value))
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
                Select( [
                    (f'{year}', year) for year in self.datefuncs.getListofYears()
                ], id="years", classes="time-input")
            ),
            HorizontalGroup(
                Label("Month: "),
                Select([
                    (f'{month[0].upper()}{month[1:]}', month) for month in self.datefuncs.getFullListofMonths()
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
        self.changeList = ChangeList()


    CSS_PATH = "test.tcss"
    LIGHT_MODE = 'textual-light'
    DARK_MODE = 'textual-dark'
    BINDINGS = [('d', 'dark_toggle', 'Toggle Dark Mode!')
    ]

    def on_mount(self):
        self.push_screen(MainScreen())

    def action_dark_toggle(self) -> None:
        self.theme = (
            self.DARK_MODE if self.theme == 'textual-light' else self.LIGHT_MODE
        )
    
EventManager().run()