from textual.app import App, ComposeResult

# from textual.reactive import reactive
from textual.containers import (
    Center,
    Container,
)
from textual.widgets import Digits, Header, Footer, Label, ProgressBar
from textual_plotext import PlotextPlot

from point_operations_training.training_set import RandValStats


class Assignement(Digits):

    stats: RandValStats = RandValStats()

    def new_mult(self):
        x, y = self.stats.next()
        self.update(f"{x} x {y}")

    def new_train(self):
        x, y = self.stats.next_train_val()
        self.update(f"{x} x {y}")


class StatPlot(PlotextPlot):

    def __init__(self, data: dict[str, list[dict[str, str | float]]]) -> None:
        self.data: dict[str, list[dict[str, str | float]]] = data
        super().__init__()

    def on_mount(self) -> None:
        # date_series = [val["date"] for val in self.data["stats"]]
        avg_series = [val["avg"] for val in self.data["stats"]]
        max_series = [val["max"] for val in self.data["stats"]]
        min_series = [val["min"] for val in self.data["stats"]]

        self.plt.plot(avg_series, label="Average")
        self.plt.plot(max_series, label="Maximum")
        self.plt.plot(min_series, label="Minimim")

        self.plt.title("Progress Plot")  # to apply a title


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

        with Center():
            yield Container()

        yield Footer()

    def action_new_mult(self) -> None:
        assignement = self.query_one(Assignement)
        progress: ProgressBar = self.query_one(ProgressBar)

        if self.assigned < LearnArithmetics.NUM_ASSIGNEMENTS:
            assignement.new_mult()
            self.assigned += 1
            progress.advance(1)
        elif self.assigned == LearnArithmetics.NUM_ASSIGNEMENTS:
            stats_label: Label = self.query_one("#stats", expect_type=Label)
            statistics = assignement.stats.statistics()
            stats_label.update(
                f"Avg: {statistics['avg']} Max: {statistics['max']} Min:{statistics['min']}"
            )
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
            _ = container.mount(StatPlot(assignement.stats.load_stats()))


if __name__ == "__main__":
    app = LearnArithmetics()
    _ = app.run()  # pyright: ignore [reportUnknownVariableType]
