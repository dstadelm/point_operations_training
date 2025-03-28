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


class TensMultiplicationAssignment:
    def __init__(self) -> None:
        self._solve_time: float = 0
        a: int = randint(0, 1)
        b: int = 1 - a
        self._assignment: tuple[int, int] = (
            10**a * randint(1, 9),
            10**b * randint(1, 9),
        )
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
        return "10x"

    @property
    def assignment(self) -> tuple[int, int]:
        return self._assignment

    @property
    def solve_time(self) -> float:
        return self.timer.duration()

    @override
    def __str__(self) -> str:
        return f"{self._assignment[0]} x {self._assignment[1]}"


class DivisionAssignment:
    def __init__(self) -> None:
        self._solve_time: float = 0
        b = randint(1, 9)
        c = randint(1, 9)
        a = b * c
        self._assignment: tuple[int, int] = (
            a,
            b,
        )
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
        return ":"

    @property
    def assignment(self) -> tuple[int, int]:
        return self._assignment

    @property
    def solve_time(self) -> float:
        return self.timer.duration()

    @override
    def __str__(self) -> str:
        return f"{self._assignment[0]} : {self._assignment[1]}"


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

    def avg_series(self) -> list[float]:
        self.sort_by_date()
        return [r.avg for r in self.results]

    def max_series(self) -> list[float]:
        self.sort_by_date()
        return [r.max for r in self.results]

    def min_series(self) -> list[float]:
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

    def avg_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].avg_series()

    def max_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].max_series()

    def min_series(self, modus_operandi: str) -> list[float]:
        return self.results[modus_operandi].min_series()

    def add_result(self, modus_operandi: str, result: Result) -> None:
        self.results.setdefault(modus_operandi, ResultCollection()).add_result(result)

    def get_results(self, modus_operandi: str) -> ResultCollection:
        return self.results[modus_operandi]

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


UserCollectionType = dict[str, dict[str, UserType] | str]


class UserCollection:
    def __init__(self) -> None:
        self.users: list[User] = []
        self.last_user: str = ""

    def to_dict(self) -> UserCollectionType:
        data: UserCollectionType = {"last_user": self.last_user, "users": {}}
        user_data = {}
        for user in self.users:
            user_data[user.name] = user.to_dict()
        data["users"] = user_data

        return data

    def from_dict(self, data: UserCollectionType) -> None:
        users: dict[str, UserType] = data.setdefault(
            "users", {}
        )  # pyright: ignore [reportAssignmentType]
        for name, value in users.items():
            user = User(name)
            user.from_dict(value)
            self.users.append(user)
        self.last_user = data.get(
            "last_user", ""
        )  # pyright: ignore [reportAttributeAccessIssue]

    def get_users(self) -> list[str]:
        return [u.name for u in self.users]

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_user(self, name: str) -> User | None:
        for user in self.users:
            if user.name == name:
                return user


DataBaseType = dict[str, UserCollectionType | str]


class DataBase:
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self.data: DataBaseType = {}

    def get_db(self) -> DataBaseType:
        if not self.data:
            if self.file.is_file():
                with open(self.file) as stats:
                    self.data = json.load(stats)

        return self.data

    def save_db(self, data: UserCollection) -> None:
        with open(self.file, "w") as stats:
            json.dump(data.to_dict(), stats)

    def get_user_collection(self) -> UserCollection:
        data = self.get_db()
        users = UserCollection()
        users.from_dict(data)  # pyright: ignore [reportArgumentType]
        return users
