from abc import ABC
from random import choices, randint
from typing import Protocol, override

from point_operations_training.utilities.timer import Timer


def get_rand_val_with_distribution() -> int:
    return choices(population=range(1, 10), weights=[1, 2, 4, 4, 4, 4, 4, 4, 4], k=1)[0]


class Assignment(ABC):

    def __init__(
        self,
        a: int = 0,
        b: int = 0,
    ) -> None:

        self.timer: Timer = Timer(name="assignment")
        self.a: int = a if a != 0 else get_rand_val_with_distribution()
        self.b: int = b if b != 0 else get_rand_val_with_distribution()
        self._assignment: tuple[int, int, int] = (0, 0, 0)
        self._modus_operandi: str = ""

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()

    @property
    def modus_operandi(self) -> str:
        return self._modus_operandi

    @property
    def assignment(self) -> tuple[int, int, int]:
        return self._assignment

    @property
    def solve_time(self) -> float:
        return self.timer.duration()

    @override
    def __str__(self) -> str:
        return f"{self._assignment[0]} {self.modus_operandi} {self._assignment[1]}"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Assignment):
            return NotImplemented
        return (
            self._assignment == other._assignment
            and self.modus_operandi == other.modus_operandi
        )


class MultiplicationAssignment(Assignment):
    def __init__(self, a: int = 0, b: int = 0) -> None:
        super().__init__(a, b)
        c: int = self.a * self.b
        self._assignment: tuple[int, int, int] = (self.a, self.b, c)
        self._modus_operandi: str = "x"


class TensMultiplicationAssignment(Assignment):
    def __init__(self, a: int = 0, b: int = 0) -> None:
        super().__init__(a, b)
        x: int = randint(0, 1)
        ax10: int = 10**x  # pyright: ignore[reportAny]
        bx10: int = 10 ** (1 - x)  # pyright: ignore[reportAny]
        ia: int = ax10 * self.a
        ib: int = bx10 * self.b
        c: int = a * b
        self._assignment: tuple[int, int, int] = (ia, ib, c)
        self._modus_operandi: str = "x"


class DivisionAssignment(Assignment):
    def __init__(self, a: int = 0, b: int = 0) -> None:
        super().__init__(a, b)
        c = self.a * self.b
        self._assignment: tuple[int, int, int] = (self.a, self.b, c)
        self._modus_operandi: str = ":"

    @override
    def __str__(self) -> str:
        return f"{self._assignment[2]} {self.modus_operandi} {self._assignment[1]}"


class AssignmentFactory(Protocol):
    def __call__(self, a: int = 0, b: int = 0) -> Assignment: ...
    @override
    def __str__(self) -> str: ...


class MultiplicationAssignmentFactory:
    def __call__(self, a: int = 0, b: int = 0) -> Assignment:
        return MultiplicationAssignment(a, b)

    @override
    def __str__(self) -> str:
        return "Multiplication"


class TensMultiplicationAssignmentFactory:
    def __call__(self, a: int = 0, b: int = 0) -> Assignment:
        return TensMultiplicationAssignment(a, b)

    @override
    def __str__(self) -> str:
        return "Multiplication x10"


class DivisionAssignmentFactory:
    def __call__(self, a: int = 0, b: int = 0) -> Assignment:
        return DivisionAssignment(a, b)

    @override
    def __str__(self) -> str:
        return "Division"


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
