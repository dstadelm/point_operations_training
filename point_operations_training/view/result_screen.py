from typing import override

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Label


class ResultScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "app.new_assignment", "New Assignment"),
    ]

    def __init__(self, results: str) -> None:
        self._results: str = results
        self.result_message: str = f"{self._results}"
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.result_message, id="result_message")
        yield Footer()

    def on_key(self) -> None:
        _ = self.dismiss()
