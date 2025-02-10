from textual.app import App, ComposeResult

# from textual.reactive import reactive
from textual.containers import (
    Center,
)
from textual.widgets import Digits, Header, Footer, Label, ProgressBar

from point_operations_training.training_set import RandValStats


class Assignement(Digits):

    stats: RandValStats = RandValStats()

    def new_mult(self):
        x, y = self.stats.next()
        self.update(f"{x} x {y}")

    def new_train(self):
        x, y = self.stats.next_train_val()
        self.update(f"{x} x {y}")


class LearnArithmetics(App):  # pyright: ignore [reportMissingTypeArgument]
    CSS_PATH = "learn.tcss"  # pyright: ignore [reportUnannotatedClassAttribute]
    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "new_mult", "Next")
    ]

    NUM_ASSIGNEMENTS: int = 20
    NUM_TRAINING: int = 20

    assigned: int = 0
    trained: int = 0

    def compose(self) -> ComposeResult:  # pyright: ignore [reportImplicitOverride]
        """Called to add widgets to the app."""
        yield Header()

        with Center():
            yield Assignement("")
        with Center():
            yield ProgressBar(total=20, show_eta=False)
        with Center():
            yield Label(id="stats")

        yield Footer()

    def action_new_mult(self) -> None:
        assignement = self.query_one(Assignement)
        progress: ProgressBar = self.query_one(ProgressBar)
        if self.assigned == LearnArithmetics.NUM_ASSIGNEMENTS:
            stats_label: Label = self.query_one("#stats", expect_type=Label)
            statistics = assignement.stats.statistics()
            stats_label.update(
                f"Avg: {statistics['avg']} Max: {statistics['max']} Min:{statistics['min']}"
            )
            # _ = vert_group.mount(
            #     Label(
            #         f"Avg: {statistics['avg']} Max: {statistics['max']} Min:{statistics['min']}",
            #         id="stats",
            #     )
            # )
            self.assigned += 1
            progress.update(total=LearnArithmetics.NUM_TRAINING, progress=0)
        elif self.assigned < LearnArithmetics.NUM_ASSIGNEMENTS:
            assignement.new_mult()
            self.assigned += 1
            progress.advance(1)
        elif self.trained < LearnArithmetics.NUM_TRAINING:
            assignement.new_train()
            progress.advance(1)
            self.trained += 1
        else:
            pass


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
