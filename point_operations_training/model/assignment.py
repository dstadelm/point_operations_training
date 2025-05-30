from abc import ABC
from random import randint
from typing import Protocol, override

from point_operations_training.timer import Timer


class Assignment(ABC):

    def __init__(self) -> None:
        self.timer: Timer = Timer(name="assignment")
        self._assignment: tuple[int, int] = (0, 0)
        self._modus_operandi: str = ""

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()

    @property
    def modus_operandi(self) -> str:
        return self._modus_operandi

    @property
    def assignment(self) -> tuple[int, int]:
        return self._assignment

    @property
    def solve_time(self) -> float:
        return self.timer.duration()

    @override
    def __str__(self) -> str:
        return f"{self._assignment[0]} {self.modus_operandi} {self._assignment[1]}"


class MultiplicationAssignment(Assignment):
    def __init__(self) -> None:
        super().__init__()
        self._assignment: tuple[int, int] = (randint(1, 9), randint(1, 9))
        self._modus_operandi: str = "x"


class TensMultiplicationAssignment(Assignment):
    def __init__(self) -> None:
        super().__init__()
        a: int = randint(0, 1)
        b: int = 1 - a
        self._assignment: tuple[int, int] = (
            10**a * randint(1, 9),
            10**b * randint(1, 9),
        )
        self._modus_operandi: str = "10x"


class DivisionAssignment(Assignment):
    def __init__(self) -> None:
        super().__init__()
        b = randint(1, 9)
        c = randint(1, 9)
        a = b * c
        self._assignment: tuple[int, int] = (
            a,
            b,
        )
        self._modus_operandi: str = ":"


class AssignmentFactory(Protocol):
    def __call__(self) -> Assignment: ...


class MultiplicationAssignmentFactory:
    def __call__(self) -> Assignment:
        return MultiplicationAssignment()


class TensMultiplicationAssignmentFactory:
    def __call__(self) -> Assignment:
        return TensMultiplicationAssignment()


class DivisionAssignmentFactory:
    def __call__(self) -> Assignment:
        return DivisionAssignment()


class AssignmentCollection:
    def __init__(self) -> None:
        self.assignments: list[Assignment] = []

    def add_assignment(self, result: Assignment) -> None:
        self.assignments.append(result)

    def avg_time(self) -> float:
        return sum([r.solve_time for r in self.assignments]) / len(self.assignments)

    def max_time(self) -> float:
        return max([r.solve_time for r in self.assignments])

    def min_time(self) -> float:
        return min([r.solve_time for r in self.assignments])

    def slowest_assignments(self, percentage: int) -> list[Assignment]:
        num = round(len(self.assignments) * percentage / 100)
        return sorted(self.assignments, key=lambda r: r.solve_time)[-num:]

    @property
    def modus_operandi(self) -> str:
        return self.assignments[0].modus_operandi

    @override
    def __str__(self) -> str:
        return f"avg: {self.avg_time()}, max: {self.max_time()}, min: {self.min_time()}"
