from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Center
from textual import on

class HorizTest(VerticalGroup):

    def compose(self) -> ComposeResult:
        yield Button("View Events", id="view_events")
        yield Button("Add Events", id="add_events")
        yield Button("Edit Events", id="edit_events")
        yield Button("Plot Events", id="plot_events")
        yield Button("Info", id="info")
        yield Button("Exit", id="exit-btn", variant="error")

class TestApp(App):

    CSS_PATH = "test.tcss"
    LIGHT_MODE = 'textual-light'
    DARK_MODE = 'textual-dark'
    BINDINGS = [('d', 'dark_toggle', 'Toggle Dark Mode!')
    ]

    @on(Button.Pressed, "#exit-btn")
    def exit_app(self):
        self.exit()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(HorizTest(), classes="buttons")

    def action_dark_toggle(self) -> None:
        self.theme = (
            self.DARK_MODE if self.theme == 'textual-light' else self.LIGHT_MODE
        )
    
TestApp().run()