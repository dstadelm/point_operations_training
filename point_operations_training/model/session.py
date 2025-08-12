from collections.abc import Generator
from datetime import datetime
from random import choices, randint

from point_operations_training.model.assignment import (
    Assignment,
    AssignmentCollection,
    AssignmentFactory,
)
from point_operations_training.model.user import User


class Session:
    def __init__(
        self,
        user: User,
        num_assignments: int = 20,
        num_training: int = 20,
    ) -> None:
        self._num_assignments: int = num_assignments
        self._num_training: int = num_training
        self._user: User = user
        self._assignment_factory: AssignmentFactory = self._user.modus.value
        self.date: str = str(datetime.now())
        self._assignments: AssignmentCollection = AssignmentCollection()
        self._current_assignement: Assignment = self._assignment_factory()
        self._slowest_assignments: list[Assignment] = []
        self._prev_idx: int = -1
        self._training_percentage: int = 20
        self._trained_assignments: int = 0
        self._last_max_idx: int = 0

    @property
    def assignments(self) -> AssignmentCollection:
        """Returns the collection of assignments."""
        return self._assignments

    def get_new_assignment(self) -> str:
        choice: int = choices([0, 1], weights=[1, 5], k=1)[0]

        if choice == 0 and self._last_max_idx < len(self._user.max_matrix):
            a, b = self._user.max_matrix[self._last_max_idx]
            self._last_max_idx += 1
            self._current_assignement = self._assignment_factory(a, b)

        else:
            if len(self._assignments.assignments) >= self._num_assignments:
                raise StopIteration()
            self._current_assignement = self._assignment_factory()
            while self._current_assignement in self._assignments.assignments:
                self._current_assignement = self._assignment_factory()

        self._current_assignement.start()
        return str(self._current_assignement)

    def commit_assignment(self) -> None:
        self._current_assignement.stop()
        self._assignments.add_assignment(self._current_assignement)

    @property
    def user_name(self) -> str:
        return self._user.name

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
