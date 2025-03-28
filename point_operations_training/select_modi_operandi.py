from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView, Static

from point_operations_training.training_set import (
    AssignmentFactory,
    DivisionAssignmentFactory,
    MultiplicationAssignmentFactory,
    TensMultiplicationAssignmentFactory,
)


class SelectModiOperandi(ModalScreen[AssignmentFactory]):

    @override
    def compose(self) -> ComposeResult:
        list_items = [
            ListItem(Label("Multiplication"), name="Multiplication"),
            ListItem(Label("Multiplication 10"), name="Multiplication 10"),
            ListItem(Label("Division"), name="Division"),
            # ListItem(Label("Division 10"), name="Division 10"),
        ]
        yield Vertical(
            Static("Select a user:", id="title"),
            ListView(*list_items, id="user-list", initial_index=0),
            id="UserSelectionDialog",
            classes="usd",
        )

    def on_list_view_selected(self, event: ListView.Selected):
        match event.item.name:
            case "Multiplication":
                _ = self.dismiss(MultiplicationAssignmentFactory())
            case "Multiplication 10":
                _ = self.dismiss(TensMultiplicationAssignmentFactory())
            case "Division":
                _ = self.dismiss(DivisionAssignmentFactory())
            # case "Division 10":
            #     _ = self.dismiss(event.item.name)
