from typing import override

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Label


class WelcomeScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "app.new_assignment", "New Assignment"),
        ("u", "app.select_user", "Select user"),
        ("o", "app.select_modi_operandi", "Select operation"),
        ("d", "app.toggle_dark", "Toggle dark mode"),
        ("q", "app.request_quit", "Quit"),
    ]

    def __init__(self, user: str) -> None:
        self._user: str = user
        if user:
            self.welcome_message: str = (
                f"Welcome back, {self._user}! Press ENTER to start!"
            )
        else:
            self.welcome_message = "Welcome! Press ENTER to start!"
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.welcome_message, id="start")
        yield Footer()

    def on_key(self) -> None:
        _ = self.dismiss()
