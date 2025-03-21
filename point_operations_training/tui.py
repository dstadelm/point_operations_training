from pathlib import Path
from typing import override

from textual.app import App, ComposeResult

# from textual.reactive import reactive
from textual.containers import Center, Container, Grid
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, ProgressBar
from textual_plotext import PlotextPlot

from point_operations_training.training_set import (
    Assignment,
    AssignmentFactory,
    DataBase,
    MultiplicationAssignmentFactory,
    Session,
    UserCollection,
)
from point_operations_training.user_selection_screen import UserSelectionScreen


class TextualAssignment(Digits):

    def __init__(self, assignment_factory: AssignmentFactory) -> None:
        super().__init__()
        self.session: Session = Session(assignment_factory)
        self.assignment: Assignment | None = None

    def new_assignement(self):
        if self.assignment:
            self.session.add_done_assignment(self.assignment)
        self.assignment = self.session.get_new_assignment()
        self.assignment.start()
        self.update(f"{self.assignment}")

    def new_train(self):
        assignement = self.session.get_next_train_assignement()
        self.update(f"{assignement}")


class StatPlot(PlotextPlot):

    def __init__(self, data: dict[str, list[dict[str, str | float]]]) -> None:
        self.data: dict[str, list[dict[str, str | float]]] = data
        super().__init__()

    @override
    def on_mount(self) -> None:
        # date_series = [val["date"] for val in self.data["stats"]]
        avg_series = [val["avg"] for val in self.data["stats"]]
        max_series = [val["max"] for val in self.data["stats"]]
        min_series = [val["min"] for val in self.data["stats"]]

        self.plt.plot(avg_series, label="Average")
        self.plt.plot(max_series, label="Maximum")
        self.plt.plot(min_series, label="Minimim")

        self.plt.title("Progress Plot")  # to apply a title


class QuitScreen(Screen):  # pyright: ignore [reportMissingTypeArgument]
    """Screen with a dialog to quit."""

    @override
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            _ = self.app.pop_screen()


class LearnArithmetics(App):  # pyright: ignore [reportMissingTypeArgument]
    CSS_PATH = "learn.tcss"  # pyright: ignore [reportUnannotatedClassAttribute]
    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "new_mult", "Next"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    NUM_ASSIGNMENTS: int = 20
    NUM_TRAINING: int = 20

    assigned: int = 0
    trained: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.db_path: Path = Path("db.json")
        self.db: DataBase = DataBase(self.db_path)
        self.user_collection: UserCollection = self.db.get_user_collection()

    def compose(self) -> ComposeResult:  # pyright: ignore [reportImplicitOverride]
        """Called to add widgets to the app."""
        yield Header()

        with Center():
            yield Label("Press ENTER to start!", id="start")
        with Center():
            yield TextualAssignment(MultiplicationAssignmentFactory())
        with Center():
            yield ProgressBar(total=20, show_eta=False)
        with Center():
            yield Label(id="stats")

        with Center():
            yield Container()

        yield Footer()

    def action_new_mult(self) -> None:
        assignement = self.query_one(TextualAssignment)
        progress: ProgressBar = self.query_one(ProgressBar)

        if self.assigned < LearnArithmetics.NUM_ASSIGNMENTS:
            start_label: Label = self.query_one("#start", expect_type=Label)
            start_label.update("")
            assignement.new_assignement()
            self.assigned += 1
            progress.advance(1)
        elif self.assigned == LearnArithmetics.NUM_ASSIGNMENTS:
            stats_label: Label = self.query_one("#stats", expect_type=Label)
            max = assignement.session.max_time()
            min = assignement.session.min_time()
            avg = assignement.session.avg_time()
            stats_label.update(f"Avg: {avg:f.2} Max: {max:f.2} Min:{min:f.2}")
            self.assigned += 1
            progress.update(total=LearnArithmetics.NUM_TRAINING, progress=0)
        elif self.trained < LearnArithmetics.NUM_TRAINING:
            assignement.new_train()
            progress.advance(1)
            self.trained += 1
        elif self.trained == LearnArithmetics.NUM_TRAINING:
            self.trained += 1
            stats_label = self.query_one("#stats", expect_type=Label)
            stats_label.update("Done")
            container = self.query_one(Container)
            # _ = container.mount(StatPlot(assignement.stats.load_db()))

    @override
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_request_quit(self) -> None:
        _ = self.push_screen(QuitScreen())

    def on_mount(self):
        _ = self.push_screen(UserSelectionScreen(["user1", "user2"]))


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
