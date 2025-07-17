from typing import override

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Label


class WelcomeScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("d", "app.toggle_dark", "Toggle dark mode"),
        ("o", "app.select_modi_operandi", "Select operation"),
        ("q", "app.request_quit", "Quit"),
        ("s", "app.show_stats", "Show statistics"),
        ("u", "app.select_user", "Select user"),
    ]

    def __init__(self, user: str, modus: str) -> None:
        self._user: str = user
        self._modus: str = modus
        if user:
            self.welcome_message: str = f"Welcome back, {self._user}!"
        else:
            self.welcome_message = "Welcome!"
        super().__init__()

    def on_mount(self) -> None:
        self.app.title = "Welcome"
        self.title = "Welcome"  # pyright: ignore [reportUnannotatedClassAttribute]
        button = self.query_one("#start_button", Button)
        button.action_scroll_end

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label(self.welcome_message, id="start")
        with Center():
            yield Label(f"Selected Modus: {self._modus}", id="modus")
        with Center():
            yield Button(
                "Start",
                variant="primary",
                id="start_button",
                action="app.new_assignment",
            )
        yield Footer()
