from collections.abc import Generator
from datetime import datetime
from random import randint

from point_operations_training.model.assignment import (
    Assignment,
    AssignmentCollection,
    AssignmentFactory,
    DivisionAssignmentFactory,
    MultiplicationAssignmentFactory,
    TensMultiplicationAssignmentFactory,
)
from point_operations_training.presenter.modi import Modi


class Session:
    def __init__(self, modus: Modi) -> None:
        match modus:
            case Modi.MULTIPLICATION:
                self._assignment_factory: AssignmentFactory = (
                    MultiplicationAssignmentFactory()
                )
            case Modi.MULTIPLICATIONx10:
                self._assignment_factory = TensMultiplicationAssignmentFactory()
            case Modi.DIVISION:
                self._assignment_factory = DivisionAssignmentFactory()
        self.date: str = str(datetime.now())
        self._assignments: AssignmentCollection = AssignmentCollection()
        self._current_assignement: Assignment = self._assignment_factory()
        self._slowest_assignments: list[Assignment] = []
        self._prev_idx: int = -1
        self._training_percentage: int = 20

    def get_new_assignment(self) -> str:
        self._current_assignement = self._assignment_factory()
        self._current_assignement.start()
        return str(self._current_assignement)

    def commit_assignment(self) -> None:
        self._current_assignement.stop()
        self._assignments.add_assignment(self._current_assignement)

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

    def get_next_train_assignement(self) -> Assignment:
        idx = randint(0, len(self.slowest_assignments(self._training_percentage)) - 1)
        while idx == self._prev_idx:
            idx = randint(
                0, len(self.slowest_assignments(self._training_percentage)) - 1
            )

        self._prev_idx = idx
        return self.slowest_assignments(self._training_percentage)[idx]

    def __iter__(self) -> Generator[Assignment, None, None]:
        for assignment in self._assignments.assignments:
            yield assignment
