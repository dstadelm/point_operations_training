from collections.abc import Generator
from datetime import datetime
from random import randint

from point_operations_training.model.assignment import (
    Assignment,
    AssignmentCollection,
    AssignmentFactory,
)


class Session:
    def __init__(self, assignement_factory: AssignmentFactory) -> None:
        self._assignment_factory: AssignmentFactory = assignement_factory
        self.date: str = str(datetime.now())
        self.assignments: AssignmentCollection = AssignmentCollection()
        self._slowest_assignments: list[Assignment] = []
        self._prev_idx: int = -1
        self._training_percentage: int = 20

    def get_new_assignment(self) -> Assignment:
        return self._assignment_factory()

    def add_done_assignment(self, assignment: Assignment) -> None:
        self.assignments.add_assignment(assignment)

    def slowest_assignments(self, percentage: int) -> list[Assignment]:
        if not self._slowest_assignments:
            self._slowest_assignments = self.assignments.slowest_assignments(percentage)
        return self._slowest_assignments

    def get_next_train_assignement(self) -> Assignment:
        idx = randint(0, len(self.slowest_assignments(self._training_percentage)) - 1)
        while idx == self._prev_idx:
            idx = randint(
                0, len(self.slowest_assignments(self._training_percentage)) - 1
            )

        self._prev_idx = idx
        return self.slowest_assignments(self._training_percentage)[idx]

    def __iter__(self) -> Generator[Assignment, None, None]:
        for assignment in self.assignments.assignments:
            yield assignment
