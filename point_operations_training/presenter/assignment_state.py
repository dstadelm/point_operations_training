from typing import override

from point_operations_training.model.result import result_from_session
from point_operations_training.model.session import Session
from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class AssignmentsState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self._presenter: PresenterProtocol = presenter
        self._session: Session = Session(self._presenter.modus)
        self._show_assignment_screen()

    def _show_assignment_screen(self) -> None:
        if self._session.solved_assignments >= self._presenter.num_assignments:
            self.store_results()
            self._presenter.switch_to_result_state(self._session)

        else:
            new_assignement: str = self._session.get_new_assignment()
            self._presenter.view.show_assignment_screen(
                user=self._presenter.user_name,
                assignment=new_assignement,
                total_assignments=self._presenter.num_assignments,
                solved_assignments=self._session.solved_assignments,
            )

    def store_results(self) -> None:
        user = self._presenter.user_collection.get_user(self._presenter.user_name)
        result = result_from_session(self._session)

        if user:
            user.add_result(str(self._presenter.modus.value), result)
            user.get_max_matrix(str(self._presenter.modus.value)).update(self._session)
        else:
            raise ValueError(f"User {self._presenter.user_name} not found")

        self._presenter.store_results()

    def start_assignments(self) -> None:
        # Commit the current assignment before starting a new one
        self._session.commit_assignment()
        self._show_assignment_screen()

    def home(self) -> None:
        self._presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
