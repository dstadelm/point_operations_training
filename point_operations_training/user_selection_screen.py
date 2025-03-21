from typing import override

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Input, Label, ListItem, ListView, Static


class UserSelectionScreen(Screen[str]):
    def __init__(self, user_list: list[str]):
        super().__init__()
        self.user_list: list[str] = user_list
        self.selected_item: str = ""

    @override
    def compose(self) -> ComposeResult:
        if not self.user_list:
            yield Grid(
                Static("Select a user:", id="title"),
                Static("No users found. Please create a new user.", id="no-users"),
                Input(placeholder="Enter new user name", id="new-user-input"),
                Button("Create User", id="create-user-button"),
                id="UserSelectionDialog",
            )
        else:
            yield Grid(
                Static("Select a user:", id="title"),
                ListView(id="user-list"),
                Button("Select User", id="select-user-button"),
                id="UserSelectionDialog",
            )

    def on_mount(self) -> None:
        if self.user_list:
            list_view = self.query_one("#user-list", ListView)
            for user in self.user_list:
                _ = list_view.append(ListItem(Label(user)))

    def on_list_view_selected(self, message: ListView.Selected):
        if message.item.name:
            self.selected_item = message.item.name
        _ = self.dismiss(self.selected_item)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-user-button":
            user_name = self.query_one("#new-user-input", Input).value
            _ = self.dismiss(user_name)
