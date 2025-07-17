from typing import override

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Input


class CreateNewUserScreen(Screen[str]):

    def __init__(self, users: list[str]) -> None:
        super().__init__()
        self.users: list[str] = users

    @override
    def compose(self) -> ComposeResult:
        yield Header(name="New User")
        yield Container(
            Input(placeholder="Enter new user name", id="new-user-input"),
            id="UserCreateDialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "Create New User"
        self.title = (  # pyright: ignore [reportUnannotatedClassAttribute]
            "Create New User"
        )

    def on_input_submitted(self, input: Input.Submitted) -> None:
        input_widget: Input = self.query_one("#new-user-input", expect_type=Input)
        if input.value in self.users:
            input_widget.clear()
            input_widget.placeholder = "User already exists. Enter new user name"
        else:
            _ = self.dismiss(input.value)
