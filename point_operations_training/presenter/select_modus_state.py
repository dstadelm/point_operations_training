from typing import override

from point_operations_training.presenter.modus import Modus
from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class SelectModusState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        self.presenter.view.show_modus_selection(self._set_modus)

    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    def _set_modus(self, modus: Modus | None) -> None:
        if modus:
            self.presenter.modus = modus
        self.presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def start_assignments(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
