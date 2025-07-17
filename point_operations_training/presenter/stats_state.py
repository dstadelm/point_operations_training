from typing import override

from point_operations_training.model.result import ResultCollectionProtocol
from point_operations_training.presenter.presenter import Presenter


class StatsState:
    def __init__(self, presenter: Presenter) -> None:
        self.presenter: Presenter = presenter
        results: ResultCollectionProtocol = self.presenter.model.get_results()

        if results:
            self.presenter.view.show_stats_screen(results)
        else:
            self.presenter.switch_to_welcome_state()

    def home(self) -> None:
        self.presenter.switch_to_welcome_state()

    def start_assignments(self) -> None: ...
    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...
    def stats(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
