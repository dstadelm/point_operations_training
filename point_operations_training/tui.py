from random import randint
from textual.app import App, ComposeResult

# from textual.reactive import reactive
from textual.widgets import Digits, Header, Footer

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

    assigned: int = 0

    def compose(self) -> ComposeResult:  # pyright: ignore [reportImplicitOverride]
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield Assignement("1 x 1", id="center-middle")

    def action_new_mult(self) -> None:
        assignement = self.query_one(Assignement)
        if self.assigned == LearnArithmetics.NUM_ASSIGNEMENTS:
            assignement.new_train()
        else:
            assignement.new_mult()
            self.assigned += 1


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
