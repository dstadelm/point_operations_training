import logging
from pathlib import Path
from typing import override

from textual.app import App, ComposeResult

# from textual.reactive import reactive
from textual.containers import Center, Container, Grid
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, ProgressBar
from textual_plotext import PlotextPlot

from point_operations_training.model.assignment import (
    Assignment,
    AssignmentFactory,
    MultiplicationAssignmentFactory,
)
from point_operations_training.model.data_base import DataBase
from point_operations_training.model.result import ResultCollection, result_from_session
from point_operations_training.model.session import Session
from point_operations_training.model.user import User, UserCollection
from point_operations_training.view.create_new_user_screen import CreateNewUser
from point_operations_training.view.select_modi_operandi import SelectModiOperandi
from point_operations_training.view.user_selection_screen import UserSelectionScreen

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TextualSession(Digits):

    def __init__(self) -> None:
        super().__init__()
        self.session: Session = Session(MultiplicationAssignmentFactory())
        self.assignment: Assignment | None = None

    def set_session(self, session: Session):
        self.assignment = None
        self.session = session
        self.update("")

    def new_assignement(self):
        if self.assignment:
            self.assignment.stop()
            print(
                f"Assignment {self.assignment} stopped with time {self.assignment.solve_time:.2f}"
            )
            self.session.add_done_assignment(self.assignment)
            for assignment in self.session.assignments.assignments:
                print(f"Assignment {assignment} with time {assignment.solve_time:.2f}")
        self.assignment = self.session.get_new_assignment()
        self.assignment.start()
        self.update(f"{self.assignment}")

    def new_train(self):
        assignement = self.session.get_next_train_assignement()
        self.update(f"{assignement}")

    def max_time(self) -> float:
        return self.session.assignments.max_time()

    def min_time(self) -> float:
        return self.session.assignments.min_time()

    def avg_time(self) -> float:
        return self.session.assignments.avg_time()


class StatPlot(PlotextPlot):

    def __init__(self, results: ResultCollection) -> None:
        self.results: ResultCollection = results
        super().__init__()

    @override
    def on_mount(self) -> None:
        # date_series = [val["date"] for val in self.data["stats"]]
        avg_series = self.results.avg_series()
        max_series = self.results.max_series()
        min_series = self.results.min_series()

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
        ("u", "select_user", "Select user"),
        ("o", "select_modi_operandi", "Select operation"),
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
        self.user_name: str = ""
        self.session: Session = Session(MultiplicationAssignmentFactory())
        self.modus_operandi: str = "*"

    def compose(self) -> ComposeResult:  # pyright: ignore [reportImplicitOverride]
        """Called to add widgets to the app."""
        yield Header()

        with Center():
            yield Label("Press ENTER to start!", id="start")
        with Center():
            yield TextualSession()
        with Center():
            yield ProgressBar(total=20, show_eta=False)
        with Center():
            yield Label(id="stats")

        with Center():
            yield Container()

        yield Footer()

    def action_new_mult(self) -> None:
        session = self.query_one(TextualSession)
        progress: ProgressBar = self.query_one(ProgressBar)

        if self.assigned < LearnArithmetics.NUM_ASSIGNMENTS:
            start_label: Label = self.query_one("#start", expect_type=Label)
            start_label.update("")
            session.new_assignement()
            self.assigned += 1
            progress.advance(1)
        elif self.assigned == LearnArithmetics.NUM_ASSIGNMENTS:
            stats_label: Label = self.query_one("#stats", expect_type=Label)
            max = session.max_time()
            min = session.min_time()
            avg = session.avg_time()
            stats_label.update(f"Avg: {avg:.2f} Max: {max:.2f} Min:{min:.2f}")
            result = result_from_session(self.session)
            self.user_collection.last_user = self.user_name
            user = self.user_collection.get_user(self.user_name)
            if user:
                user.add_result(self.modus_operandi, result)
                user.get_max_matrix(self.modus_operandi).update(self.session)
            else:
                raise ValueError(f"User {self.user_name} not found")

            self.db.save_db(self.user_collection)
            self.assigned += 1
            progress.update(total=LearnArithmetics.NUM_TRAINING, progress=0)
        elif self.trained < LearnArithmetics.NUM_TRAINING:
            session.new_train()
            progress.advance(1)
            self.trained += 1
        elif self.trained == LearnArithmetics.NUM_TRAINING:
            self.trained += 1
            stats_label = self.query_one("#stats", expect_type=Label)
            stats_label.update("Done")
            container = self.query_one(Container)
            user = self.user_collection.get_user(self.user_name)
            if user:
                _ = container.mount(StatPlot(user.get_results(self.modus_operandi)))

    @override
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (  # pyright: ignore [reportUnannotatedClassAttribute]
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_request_quit(self) -> None:
        _ = self.push_screen(QuitScreen())

    def on_mount(self):
        textual_session = self.query_one(TextualSession)
        textual_session.set_session(self.session)
        self.user_name = self.user_collection.last_user
        if not self.user_name:
            self.action_select_user()
        else:
            self.query_one("#start", expect_type=Label).update(
                f"Hello {self.user_name}! Press ENTER to start!"
            )

    def action_select_user(self) -> None:
        users = [user.name for user in self.user_collection.users]

        def set_user(value: str | None):
            if value:
                self.user_name = value
                if self.user_name not in users:
                    new_user = User(self.user_name)
                    self.user_collection.add_user(new_user)
            else:
                _ = self.push_screen(CreateNewUser(users), callback=set_user)

            self.reset()

        if users:
            _ = self.push_screen(UserSelectionScreen(users), callback=set_user)
        else:
            _ = self.push_screen(CreateNewUser(users), callback=set_user)

    def action_select_modi_operandi(self) -> None:
        def set_modi_operandi(factory: AssignmentFactory | None):
            if factory:
                self.session = Session(factory)
                self.modus_operandi = factory().modus_operandi
                self.reset()
            else:
                _ = self.push_screen(SelectModiOperandi(), callback=set_modi_operandi)

        _ = self.push_screen(SelectModiOperandi(), callback=set_modi_operandi)

    def reset(self):
        self.assigned = 0
        self.trained = 0
        self.query_one(TextualSession).set_session(self.session)
        progress: ProgressBar = self.query_one(ProgressBar)
        progress.update(total=LearnArithmetics.NUM_ASSIGNMENTS, progress=0)
        self.query_one("#start", expect_type=Label).update(
            f"Hello {self.user_name}! Press ENTER to start!"
        )


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
