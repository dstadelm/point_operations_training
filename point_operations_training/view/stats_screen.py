from typing import override

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Footer, Header
from textual_plotext import PlotextPlot

from point_operations_training.model.result import ResultCollectionProtocol


class StatsScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("escape", "app.home", "Home"),
        ("q", "app.request_quit", "Quit"),
    ]

    def __init__(self, results: ResultCollectionProtocol) -> None:
        self._results: ResultCollectionProtocol = results
        self.result_message: str = f"{self._results}"
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield PlotextPlot()
        yield Footer()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt

        avg_series = self._results.avg_series()
        max_series = self._results.max_series()
        min_series = self._results.min_series()

        plt.plot(avg_series, label="Average")
        plt.plot(max_series, label="Maximum")
        plt.plot(min_series, label="Minimim")

        plt.title("Progress Plot")  # to apply a title

    def on_key(self) -> None:
        _ = self.dismiss()
