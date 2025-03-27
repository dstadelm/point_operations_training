from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListItem, ListView, Static


class UserSelectionScreen(ModalScreen[str]):
    def __init__(self, user_list: list[str]):
        super().__init__()
        self.user_list: list[str] = user_list
        self.selected_item: str = ""

    @override
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Select a user:", id="title"),
            ListView(id="user-list", initial_index=0),
            id="UserSelectionDialog",
            classes="usd",
        )

    def on_mount(self) -> None:
        list_view = self.query_one("#user-list", ListView)
        if self.user_list:
            for user in self.user_list:
                _ = list_view.append(ListItem(Label(user), name=user))
        list_view.append(ListItem(Label("<create new user>"), name="<create new user>"))
        list_view.id

    def on_list_view_selected(self, event: ListView.Selected):
        _ = self.dismiss(event.item.name)
