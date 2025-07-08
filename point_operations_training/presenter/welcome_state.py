from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class WelcomeState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        if self.presenter.user_name:
            self.presenter.view.show_welcome_screen(
                self.presenter.user_name, str(self.presenter.modus.value)
            )
        else:
            self.presenter.switch_to_create_user_state()

    def select_user(self) -> None:
        """Switch state to SelectUserState."""
        self.presenter.switch_to_select_user_state()

    def select_modi_operandi(self) -> None:
        """Switch state to SelectModiOperandiState."""
        self.presenter.switch_to_select_modus_state()

    def start_assignments(self) -> None:
        """Switch state to StartAssignmentsState."""
        self.presenter.switch_to_assignment_state()

    def create_user(self) -> None:
        """Switch state to CreateNewUserState."""
        self.presenter.switch_to_create_user_state()

    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
