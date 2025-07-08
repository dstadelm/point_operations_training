from typing import override

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Label


class WelcomeScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("u", "app.select_user", "Select user"),
        ("o", "app.select_modi_operandi", "Select operation"),
        ("d", "app.toggle_dark", "Toggle dark mode"),
        ("q", "app.request_quit", "Quit"),
    ]

    def __init__(self, user: str, modus: str) -> None:
        self._user: str = user
        self._modus: str = modus
        if user:
            self.welcome_message: str = f"Welcome back, {self._user}!"
        else:
            self.welcome_message = "Welcome!"
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label(self.welcome_message, id="start")
        with Center():
            yield Label(f"Selected Modus: {self._modus}", id="modus")
        with Center():
            yield Button("Start", variant="primary", id="start_button")
        yield Footer()

    async def on_button_pressed(self) -> None:
        _ = await self.app.run_action("new_assignment")
