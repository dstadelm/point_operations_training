from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView, Static


class UserSelectionScreen(ModalScreen[str]):
    def __init__(self, user_list: list[str]):
        super().__init__()
        self.user_list: list[str] = user_list
        self.selected_item: str = ""

    @override
    def compose(self) -> ComposeResult:
        list_items = [ListItem(Label(user), name=user) for user in self.user_list]
        list_items.append(ListItem(Label("<create new user>"), name=""))
        yield Vertical(
            Static("Select a user:", id="title"),
            ListView(*list_items, id="user-list", initial_index=0),
            id="UserSelectionDialog",
            classes="usd",
        )

    def on_list_view_selected(self, event: ListView.Selected):
        _ = self.dismiss(event.item.name)
