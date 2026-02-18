from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class TestApp(App):

    LIGHT_MODE = 'textual-light'
    DARK_MODE = 'textual-dark'
    BINDINGS = [('d', 'dark_toggle', 'Toggle Dark Mode!'),
                ('q', 'exit', "Exit App")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_dark_toggle(self) -> None:
        self.theme = (
            self.DARK_MODE if self.theme == 'textual-light' else self.LIGHT_MODE
        )

    # def exit(self) -> None:
    #     self.exit()
    
TestApp().run()