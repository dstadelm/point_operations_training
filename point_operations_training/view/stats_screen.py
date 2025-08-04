from typing import override

import matplotlib.pyplot as mplt
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header
from textual_plotext import PlotextPlot

from point_operations_training.model.result import ResultCollectionProtocol


class StatsScreen(ModalScreen[str]):

    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("h", "app.home", "Home"),
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
        with Center():
            yield Button("External Viewer", variant="primary", id="matplotlib_button")
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "Statistics"
        self.title = "Statistics"  # pyright: ignore [reportUnannotatedClassAttribute]
        plt = self.query_one(PlotextPlot).plt

        avg_series = self._results.avg_series()
        max_series = self._results.max_series()
        min_series = self._results.min_series()

        plt.plot(avg_series, label="Average")
        plt.plot(max_series, label="Maximum")
        plt.plot(min_series, label="Minimim")

        plt.title("Progress Plot")  # to apply a title

    def on_button_pressed(self) -> None:
        avg_series = self._results.avg_series()
        max_series = self._results.max_series()
        min_series = self._results.min_series()

        mplt.style.use("dark_background")
        _, ax = mplt.subplots()  # pyright: ignore [reportUnknownMemberType]
        (avg_plot,) = ax.plot(avg_series)  # pyright: ignore [reportUnknownMemberType]
        (max_plot,) = ax.plot(max_series)  # pyright: ignore [reportUnknownMemberType]
        (min_plot,) = ax.plot(min_series)  # pyright: ignore [reportUnknownMemberType]
        _ = ax.legend(  # pyright: ignore [reportUnknownMemberType]
            (avg_plot, max_plot, min_plot),
            ("avg", "max", "min"),
            loc="upper right",
            shadow=True,
        )
        mplt.show()  # pyright: ignore [reportUnknownMemberType]
