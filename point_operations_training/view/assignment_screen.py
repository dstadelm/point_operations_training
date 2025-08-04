from typing import override

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Digits, Footer, Header, ProgressBar


class AssignmentScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "app.new_assignment", "Next"),
        ("h", "app.home", "Home"),
        ("q", "app.request_quit", "Quit"),
    ]

    def __init__(
        self,
        user: str,
        assignement: str,
        total_assignments: int,
        solved_assignments: int,
    ) -> None:
        super().__init__()
        self.user: str = user
        self.assignement: str = assignement
        self.total_assignments: int = total_assignments
        self.solved_assignments: int = solved_assignments

    @override
    def compose(self) -> ComposeResult:
        yield Header(name="Assignment")
        with Center():
            yield Digits(id="assignment", value=self.assignement)
        with Center():
            yield ProgressBar(total=20, show_eta=False, id="progress")
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "Assignment"
        self.title = "Assignment"  # pyright: ignore [reportUnannotatedClassAttribute]
        progress: ProgressBar = self.query_one(ProgressBar)
        progress.update(total=self.total_assignments, progress=self.solved_assignments)
