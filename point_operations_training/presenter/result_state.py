from typing import override

from point_operations_training.presenter.presenter import Presenter


class ResultState:
    def __init__(self, presenter: Presenter) -> None:
        self._presenter: Presenter = presenter
        min = self._presenter.model.session_min()
        max = self._presenter.model.session_max()
        avg = self._presenter.model.session_avg()

        result_message = f"Min = {min:.2f} s, Max = {max:.2f} s, Avg = {avg:.2f} s"

        self._presenter.view.show_result_screen(result_message)

    def start_assignments(self) -> None:
        self._presenter.switch_to_training_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...
    def home(self) -> None: ...
    def stats(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
