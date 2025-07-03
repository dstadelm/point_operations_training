from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol
from point_operations_training.presenter.state import State


class AssignmentsState(State):
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        # Here you would initialize the assignment logic
        # For example, starting a new session or showing assignments
        self.show_assignment_screen()

    def show_assignment_screen(self) -> None:
        new_assignement: str = self.presenter.session.get_new_assignment()
        self.presenter.view.show_assignment_screen(
            user=self.presenter.user_name,
            assignment=new_assignement,
            total_assignments=self.presenter.num_assignments,
            solved_assignments=self.presenter.session.solved_assignments,
        )

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
        """Already in AssignmentsState, no action needed."""
        self.presenter.commit_assignment()
        self.show_assignment_screen()

    @override
    def create_user(self) -> None:
        """Switch state to CreateNewUserState."""
        self.presenter.switch_to_create_user_state()

    @override
    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()
