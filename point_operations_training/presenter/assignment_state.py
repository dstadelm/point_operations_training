from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class AssignmentsState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self._presenter: PresenterProtocol = presenter
        self._presenter.model.start_session()
        self._show_assignment_screen()

    def _show_assignment_screen(self) -> None:

        try:
            new_assignement: str = self._presenter.model.get_new_assignment()
            solved, total = self._presenter.model.get_solved_progress()
            self._presenter.view.show_assignment_screen(
                user=self._presenter.user_name,
                assignment=new_assignement,
                total_assignments=total,
                solved_assignments=solved,
            )
        except StopIteration:
            self._presenter.model.save_session()
            self._presenter.switch_to_result_state()

    def start_assignments(self) -> None:
        # Commit the current assignment before starting a new one
        self._presenter.model.commit_assignment()
        self._show_assignment_screen()

    def home(self) -> None:
        self._presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...
    def stats(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
