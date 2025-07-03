from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol
from point_operations_training.presenter.state import State


class InitState(State):
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter

    @override
    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.view.show_welcome_screen(self.presenter.user_name)

    @override
    def select_user(self) -> None: ...
    @override
    def select_modi_operandi(self) -> None: ...
    @override
    def start_assignments(self) -> None: ...
    @override
    def create_user(self) -> None: ...
