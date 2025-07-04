from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from point_operations_training.presenter.modi import Modi


class SelectModus(ModalScreen[Modi]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("escape", "app.home", "Home"),
        ("u", "app.select_user", "Select user"),
        ("q", "app.request_quit", "Quit"),
    ]

    @override
    def compose(self) -> ComposeResult:
        list_items = [
            ListItem(Label(Modi.MULTIPLICATION.value), name=Modi.MULTIPLICATION.value),
            ListItem(
                Label(Modi.MULTIPLICATIONx10.value), name=Modi.MULTIPLICATIONx10.value
            ),
            ListItem(Label(Modi.DIVISION.value), name=Modi.DIVISION.value),
            # ListItem(Label("Division 10"), name="Division 10"),
        ]
        yield Header(name="Modus Operandi")
        yield Vertical(
            Static("Select a user:", id="title"),
            ListView(*list_items, id="user-list", initial_index=0),
            id="UserSelectionDialog",
            classes="usd",
        )
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected):
        match event.item.name:
            case Modi.MULTIPLICATION.value:
                _ = self.dismiss(Modi.MULTIPLICATION)
            case "Multiplication 10":
                _ = self.dismiss(Modi.MULTIPLICATIONx10)
            case "Division":
                _ = self.dismiss(Modi.DIVISION)
            case _:
                raise ValueError
