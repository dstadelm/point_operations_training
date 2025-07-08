from typing import override

from point_operations_training.model.assignment import Assignment
from point_operations_training.model.session import Session
from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class TrainingState:
    def __init__(self, presenter: PresenterProtocol, session: Session) -> None:
        self.presenter: PresenterProtocol = presenter
        self._session: Session = session
        self._num_training_assignments: int = 0
        self._show_assignment_screen()

    def _show_assignment_screen(self) -> None:
        if self._num_training_assignments >= self.presenter.num_training:
            self.presenter.switch_to_stats_state()
        else:
            assignment: Assignment = self._session.get_next_train_assignement()

            self.presenter.view.show_assignment_screen(
                user=self.presenter.user_name,
                assignment=str(assignment),
                total_assignments=self.presenter.num_assignments,
                solved_assignments=self._num_training_assignments,
            )
            self._num_training_assignments += 1

    def start_assignments(self) -> None:
        self._show_assignment_screen()

    def home(self) -> None:
        self.presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
