from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class InitState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter

    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def start_assignments(self) -> None: ...
    def create_user(self) -> None: ...
    def stats(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
