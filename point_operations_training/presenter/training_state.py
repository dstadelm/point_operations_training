from typing import override

from point_operations_training.presenter.presenter import Presenter


class TrainingState:
    def __init__(self, presenter: Presenter) -> None:
        self._presenter: Presenter = presenter
        self._num_training_assignments: int = 0
        self._show_assignment_screen()

    def _show_assignment_screen(self) -> None:
        # if self._num_training_assignments >= self._presenter.num_training:
        #     self._presenter.switch_to_stats_state()
        try:
            assignment: str = self._presenter.model.get_next_train_assignment()
            solved, total = self._presenter.model.get_training_progress()

            self._presenter.view.show_assignment_screen(
                user=self._presenter.user_name,
                assignment=assignment,
                total_assignments=total,
                solved_assignments=solved,
            )
            self._num_training_assignments += 1
        except StopIteration:
            self._presenter.switch_to_stats_state()

    def start_assignments(self) -> None:
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
