from collections.abc import Generator
from datetime import datetime
from random import randint

from point_operations_training.model.assignment import (
    Assignment,
    AssignmentCollection,
    AssignmentFactory,
)
from point_operations_training.presenter.modus import Modus


class Session:
    def __init__(
        self,
        user_name: str,
        modus: Modus,
        num_assignments: int = 20,
        num_training: int = 20,
    ) -> None:
        self._num_assignments: int = num_assignments
        self._num_training: int = num_training
        self._user_name: str = user_name
        self._assignment_factory: AssignmentFactory = modus.value
        self.date: str = str(datetime.now())
        self._assignments: AssignmentCollection = AssignmentCollection()
        self._current_assignement: Assignment = self._assignment_factory()
        self._slowest_assignments: list[Assignment] = []
        self._prev_idx: int = -1
        self._training_percentage: int = 20
        self._trained_assignments: int = 0

    def get_new_assignment(self) -> str:
        if len(self._assignments.assignments) >= self._num_assignments:
            raise StopIteration()
        self._current_assignement = self._assignment_factory()
        self._current_assignement.start()
        return str(self._current_assignement)

    def commit_assignment(self) -> None:
        self._current_assignement.stop()
        self._assignments.add_assignment(self._current_assignement)

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def max(self) -> float:
        return self._assignments.max_time()

    @property
    def min(self) -> float:
        return self._assignments.min_time()

    @property
    def avg(self) -> float:
        return self._assignments.avg_time()

    @property
    def solved_assignments(self) -> int:
        return len(self._assignments.assignments)

    def slowest_assignments(self, percentage: int) -> list[Assignment]:
        if not self._slowest_assignments:
            self._slowest_assignments = self._assignments.slowest_assignments(
                percentage
            )
        return self._slowest_assignments

    def get_next_train_assignement(self) -> str:
        if self._trained_assignments >= self._num_training:
            raise StopIteration()

        idx = randint(0, len(self.slowest_assignments(self._training_percentage)) - 1)
        while idx == self._prev_idx:
            idx = randint(
                0, len(self.slowest_assignments(self._training_percentage)) - 1
            )

        self._prev_idx = idx
        self._trained_assignments += 1
        return str(self.slowest_assignments(self._training_percentage)[idx])

    def get_solved_progress(self) -> tuple[int, int]:
        return len(self._assignments.assignments) + 1, self._num_assignments

    def get_training_progress(self) -> tuple[int, int]:
        return self._trained_assignments, self._num_training

    def __iter__(self) -> Generator[Assignment, None, None]:
        for assignment in self._assignments.assignments:
            yield assignment
