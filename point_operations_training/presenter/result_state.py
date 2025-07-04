from typing import override

from point_operations_training.model.session import Session
from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class ResultState:
    def __init__(self, presenter: PresenterProtocol, session: Session) -> None:
        self.presenter: PresenterProtocol = presenter
        self._session: Session = session
        min = self._session.min
        max = self._session.max
        avg = self._session.avg

        result_message = f"Min = {min:.2f} s, Max = {max:.2f} s, Avg = {avg:.2f} s"

        self.presenter.view.show_result_screen(result_message)

    def start_assignments(self) -> None:
        self.presenter.switch_to_training_state(self._session)

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...
    def home(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
