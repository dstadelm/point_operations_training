import json
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Protocol, override

from point_operations_training.timer import Timer


class Assignment(Protocol):

    def start(self) -> None: ...

    def stop(self) -> None: ...

    @property
    def modus_operandi(self) -> str: ...

    @property
    def assignment(self) -> tuple[int, int]: ...

    @property
    def solve_time(self) -> float: ...

    @override
    def __str__(self) -> str: ...


class MultiplicationAssignment:
    def __init__(self) -> None:
        self._solve_time: float = 0
        self._assignment: tuple[int, int] = (randint(1, 9), randint(1, 9))
        self.timer: Timer = Timer(name="assignment")

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        if self._solve_time == 0:
            self.timer.stop()

    def to_dict(self) -> dict[float, tuple[int, int]]:
        return {self._solve_time: self._assignment}

    def from_dict(self, data: dict[float, tuple[int, int]]) -> None:
        self._solve_time = list(data.keys())[0]
        self._assignment = list(data.values())[0]

    @property
    def modus_operandi(self) -> str:
        return "x"

    @property
    def assignment(self) -> tuple[int, int]:
        return self._assignment

    @property
    def solve_time(self) -> float:
        return self.timer.duration()

    @override
    def __str__(self) -> str:
        return f"{self._assignment[0]} x {self._assignment[1]}"


class AssignmentFactory(Protocol):
    def __call__(self) -> Assignment: ...


class MultiplicationAssignmentFactory:
    def __call__(self) -> Assignment:
        return MultiplicationAssignment()


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


class Session:
    def __init__(self, assignement_factory: AssignmentFactory) -> None:
        self.assignment_factory: AssignmentFactory = assignement_factory
        self.date: str = str(datetime.now())
        self.assignments: AssignmentCollection = AssignmentCollection()
        self._slowest_assignments: list[Assignment] = []
        self.prev_idx: int = -1
        self.training_percentage: int = 20

    def get_new_assignment(self) -> Assignment:
        return self.assignment_factory()

    def add_done_assignment(self, assignment: Assignment) -> None:
        self.assignments.add_assignment(assignment)

    def slowest_assignments(self, percentage: int) -> list[Assignment]:
        if not self._slowest_assignments:
            self._slowest_assignments = self.assignments.slowest_assignments(percentage)
        return self._slowest_assignments

    def get_next_train_assignement(self) -> Assignment:
        idx = randint(0, len(self.slowest_assignments(self.training_percentage)) - 1)
        while idx == self.prev_idx:
            idx = randint(
                0, len(self.slowest_assignments(self.training_percentage)) - 1
            )

        self.prev_idx = idx
        return self.slowest_assignments(self.training_percentage)[idx]

    def __iter__(self) -> Generator[Assignment, None, None]:
        for assignment in self.assignments.assignments:
            yield assignment


class Result:
    def __init__(
        self,
        date: str = "",
        avg: float = 0,
        max: float = 0,
        min: float = 0,
    ) -> None:
        self.date: str = str(datetime.now())
        self.avg: float = avg
        self.max: float = max
        self.min: float = min


def result_from_session(session: Session) -> Result:
    return Result(
        session.date,
        session.assignments.avg_time(),
        session.assignments.max_time(),
        session.assignments.min_time(),
    )


ResultCollectionType = list[dict[str, str | float]]


class ResultCollection:
    def __init__(self) -> None:
        self.results: list[Result] = []

    def add_result(self, result: Result) -> None:
        self.results.append(result)

    def sort_by_date(self) -> None:
        self.results.sort(key=lambda r: r.date)

    def get_avg_series(self) -> list[float]:
        self.sort_by_date()
        return [r.avg for r in self.results]

    def get_max_series(self) -> list[float]:
        self.sort_by_date()
        return [r.max for r in self.results]

    def get_min_series(self) -> list[float]:
        self.sort_by_date()
        return [r.min for r in self.results]

    def to_dict(self) -> ResultCollectionType:
        return [
            {
                "date": r.date,
                "avg": r.avg,
                "max": r.max,
                "min": r.min,
            }
            for r in self.results
        ]

    def from_dict(self, data: ResultCollectionType) -> None:
        for d in data:
            r = Result(
                str(d["date"]),
                float(d["avg"]),
                float(d["max"]),
                float(d["min"]),
            )
            self.add_result(r)


MaxMatrixType = dict[str, float]


class MaxMatrix:
    def __init__(self) -> None:
        self.matrix: MaxMatrixType = {}

    def tuple2key(self, t: tuple[int, int]) -> str:
        return f"{t[0]},{t[1]}"

    def key2tuple(self, key: str) -> tuple[int, ...]:
        return tuple([int(x) for x in key.split(",")])

    def update(self, session: Session) -> None:
        for assignment in session:
            current_value = self.matrix.setdefault(
                self.tuple2key(assignment.assignment), 0
            )
            new_value = (
                assignment.solve_time
                if assignment.solve_time > current_value
                else current_value
            )
            self.matrix[self.tuple2key(assignment.assignment)] = new_value

    def sort_by_value(self) -> None:
        self.matrix = dict(reversed(sorted(self.matrix.items(), key=lambda x: x[1])))

    def get_worst_n_percent(self, percentage: int) -> list[tuple[int, ...]]:
        self.sort_by_value()
        num_values = int(len(self.matrix) * percentage / 100)
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]

    def get_worst_n(self, num_values: int) -> list[tuple[int, ...]]:
        self.sort_by_value()
        return [self.key2tuple(key) for key in list(self.matrix.keys())[:num_values]]


UserType = dict[str, dict[str, ResultCollectionType | MaxMatrixType]]


class User:
    def __init__(self, name: str = "") -> None:
        self.name: str = name
        self.results: dict[str, ResultCollection] = {}
        self.max_matrices: dict[str, MaxMatrix] = {}

    def get_max_matrix(self, modus_operandi: str) -> MaxMatrix:
        return self.max_matrices.setdefault(modus_operandi, MaxMatrix())

    def get_avg_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].get_avg_series()

    def get_max_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].get_max_series()

    def get_min_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].get_min_series()

    def add_result(self, modus_operandi: str, result: Result) -> None:
        self.results.setdefault(modus_operandi, ResultCollection()).add_result(result)

    def from_dict(
        self,
        data: UserType,
    ) -> None:
        for modus_operandi in data.keys():
            for key, value in data[modus_operandi].items():
                if key == "results":
                    self.results[modus_operandi] = ResultCollection()
                    self.results[modus_operandi].from_dict(
                        value  # pyright: ignore [reportArgumentType]
                    )
                if key == "max_matrix":
                    self.max_matrices[modus_operandi] = MaxMatrix()
                    self.max_matrices[modus_operandi].matrix = (
                        value  # pyright: ignore [reportAttributeAccessIssue]
                    )

    def to_dict(self) -> UserType:
        data: UserType = {}
        for modus_operandi, result in self.results.items():
            data[modus_operandi] = {}
            data[modus_operandi]["results"] = result.to_dict()
            data[modus_operandi]["max_matrix"] = self.max_matrices[
                modus_operandi
            ].matrix

        return data


UserCollectionType = dict[str, UserType]


class UserCollection:
    def __init__(self) -> None:
        self.users: list[User] = []

    def to_dict(self) -> UserCollectionType:
        data: UserCollectionType = {}
        for user in self.users:
            data[user.name] = user.to_dict()

        return data

    def from_dict(self, data: UserCollectionType) -> None:
        for name, value in data.items():
            user = User(name)
            user.from_dict(value)
            self.users.append(user)

    def get_users(self) -> list[str]:
        return [u.name for u in self.users]

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_user(self, name: str) -> User | None:
        for user in self.users:
            if user.name == name:
                return user


class DataBase:
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self.data: UserCollectionType = {}

    def get_db(self) -> UserCollectionType:
        if not self.data:
            if self.file.is_file():
                with open(self.file) as stats:
                    self.data = json.load(stats)

        return self.data

    def save_db(self, data: UserCollection) -> None:
        with open(self.file, "w") as stats:
            json.dump(data.to_dict(), stats)

    def get_user_collection(self) -> UserCollection:
        data: UserCollectionType = self.get_db()
        users = UserCollection()
        users.from_dict(data)
        return users
