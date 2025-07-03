from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol
from point_operations_training.presenter.state import State


class CreateNewUserState(State):
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        self.presenter.view.show_create_new_user(self.presenter.users, self.add_user)

    @override
    def select_user(self) -> None:
        """Switch state to SelectUserState."""
        self.presenter.switch_to_select_user_state()

    @override
    def select_modi_operandi(self) -> None:
        """Switch state to SelectModiOperandiState."""
        self.presenter.switch_to_select_modus_state()

    @override
    def start_assignments(self) -> None:
        """Not possible in this state."""
        ...

    @override
    def create_user(self) -> None:
        """Switch state to CreateNewUserState."""
        self.presenter.switch_to_create_user_state()

    @override
    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    def add_user(self, name: str | None) -> None:
        if name:
            self.presenter.user_name = name
        self.presenter.switch_to_welcome_state()
