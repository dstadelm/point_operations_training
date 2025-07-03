from typing import override

from point_operations_training.model.assignment import AssignmentFactory
from point_operations_training.presenter.presenter_protocol import PresenterProtocol
from point_operations_training.presenter.state import State


class SelectModusState(State):
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        self.presenter.view.show_modi_operandi_selection(self.set_modus)

    @override
    def select_user(self) -> None:
        """Switch state to SelectUserState."""
        self.presenter.switch_to_select_user_state()

    @override
    def start_assignments(self) -> None:
        """Switch state to StartAssignmentsState."""
        self.presenter.switcht_to_assignment_state()

    @override
    def select_modi_operandi(self) -> None:
        """Switch state to SelectModiOperandiState."""
        self.presenter.switch_to_select_modus_state()

    @override
    def create_user(self) -> None:
        """Switch state to CreateNewUserState."""
        self.presenter.switch_to_create_user_state()

    @override
    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    def set_modus(self, factory: AssignmentFactory | None) -> None:
        if factory:
            self.presenter.modus_operandi = factory
        self.presenter.switch_to_welcome_state()
