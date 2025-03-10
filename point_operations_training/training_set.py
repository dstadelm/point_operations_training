import json
from collections.abc import Generator
from copy import copy
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Protocol, override

from point_operations_training.timer import Timer


class Assignment(Protocol):
    solve_time: float
    assignment: tuple[int, int]

    def new(self) -> tuple[int, int]: ...

    def done(self) -> None: ...


class MultiplicationAssignment:
    def __init__(self) -> None:
        self.solve_time: float = 0
        self.assignment: tuple[int, int] = (randint(1, 9), randint(1, 9))
        self.timer: Timer = Timer(name="assignment")

    def start(self) -> tuple[int, int]:
        self.timer.start()
        return self.assignment

    def stop(self) -> None:
        if self.solve_time == 0:
            self.solve_time = self.timer.duration()

    def to_dict(self) -> dict[float, tuple[int, int]]:
        return {self.solve_time: self.assignment}

    def from_dict(self, data: dict[float, tuple[int, int]]) -> None:
        self.solve_time = list(data.keys())[0]
        self.assignment = list(data.values())[0]


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

    def slowest_assignments(self, percentage: float) -> list[tuple[int, int]]:
        num = round(len(self.assignments) * percentage)
        return [
            r.assignment
            for r in sorted(self.assignments, key=lambda r: r.solve_time)[-num:]
        ]

    @override
    def __str__(self) -> str:
        return f"avg: {self.avg_time()}, max: {self.max_time()}, min: {self.min_time()}"


class Session:
    def __init__(self, assignement_cls: type[Assignment]) -> None:
        self.assignement_cls: type[Assignment] = assignement_cls
        self.date: str = str(datetime.now())
        self.assignments: AssignmentCollection = AssignmentCollection()
        self.assignment: Assignment = (
            None  # pyright: ignore [reportAttributeAccessIssue]
        )

    def get_assignment(self) -> tuple[int, int]:
        self.assignment = self.assignement_cls()
        return self.assignment.assignment

    def assignment_done(self) -> None:
        self.assignment.done()
        self.assignments.add_assignment(copy(self.assignment))

    def avg_time(self) -> float:
        return self.assignments.avg_time()

    def max_time(self) -> float:
        return self.assignments.max_time()

    def min_time(self) -> float:
        return self.assignments.min_time()

    def slowest_assignments(self, percentage: float) -> list[tuple[int, int]]:
        return self.assignments.slowest_assignments(percentage)

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
        session.date, session.avg_time(), session.max_time(), session.min_time()
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

    def to_dict(self) -> list[dict[str, str | float]]:
        return [
            {"date": r.date, "avg": r.avg, "max": r.max, "min": r.min}
            for r in self.results
        ]

    def from_dict(self, data: ResultCollectionType) -> None:
        for d in data:
            r = Result(
                str(d["date"]), float(d["avg"]), float(d["max"]), float(d["min"])
            )
            self.add_result(r)


MaxMatrixType = dict[tuple[int, int], float]


class MaxMatrix:
    def __init__(self) -> None:
        self.matrix: MaxMatrixType = {}

    def update(self, session: Session) -> None:
        for assignment in session:
            current_value = self.matrix.setdefault(assignment.assignment, 0)
            new_value = (
                assignment.solve_time
                if assignment.solve_time > current_value
                else current_value
            )
            self.matrix[assignment.assignment] = new_value

    def sort_by_value(self) -> None:
        self.matrix = dict(reversed(sorted(self.matrix.items(), key=lambda x: x[1])))

    def get_worst_n_percent(self, percentage: int) -> list[tuple[int, int]]:
        self.sort_by_value()
        num_values = int(len(self.matrix) * percentage / 100)
        return list(self.matrix.keys())[:num_values]


UserType = dict[str, str | MaxMatrixType | ResultCollectionType]


class User:
    def __init__(self, name: str = "") -> None:
        self.name: str = name
        self.results: ResultCollection = ResultCollection()
        self.max_matrix: MaxMatrix = MaxMatrix()

    def get_avg_series(self) -> list[float]:
        return self.results.get_avg_series()

    def get_max_series(self) -> list[float]:
        return self.results.get_max_series()

    def get_min_series(self) -> list[float]:
        return self.results.get_min_series()

    def add_result(self, result: Result) -> None:
        self.results.add_result(result)

    def from_dict(
        self,
        data: UserType,
    ) -> None:
        self.name = str(data["user"])
        self.results.from_dict(data["results"])  # pyright: ignore [reportArgumentType]
        self.max_matrix.matrix = data[
            "max_matrix"
        ]  # pyright: ignore [reportAttributeAccessIssue]


UserCollectionType = list[UserType]


class UserCollection:
    def __init__(self) -> None:
        self.users: list[User] = []

    def to_dict(self) -> dict[str, list[dict[str, str | float]]]:
        return {u.name: u.results.to_dict() for u in self.users}

    def from_dict(self, data: UserCollectionType) -> None:
        for users in data:
            user = User()
            user.from_dict(users)
            self.users.append(user)

    def get_users(self) -> list[str]:
        return [u.name for u in self.users]

    def get_user(self, name: str) -> User:
        for user in self.users:
            if user.name == name:
                return user

        user = User(name)
        self.users.append(user)
        return user


class DataBase:
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self.data: UserCollectionType = []

    def get_db(self) -> UserCollectionType:
        if not self.data:
            if self.file.is_file():
                with open(self.file) as stats:
                    self.data = json.load(stats)

        return self.data

    def save_db(self, data: dict[str, list[dict[str, str | float]]]) -> None:
        with open(self.file, "w") as stats:
            json.dump(data, stats)

    def get_user_collection(self) -> UserCollection:
        data: UserCollectionType = self.get_db()
        users = UserCollection()
        users.from_dict(data)
        return users


# class RandValStats:
#
#     SELECTION_FRACTION: float = 0.2
#
#     def __init__(self) -> None:
#         self.measured_times: dict[float, tuple[int, int]] = {}
#         self._session_stats: dict[str, str | float] = {}
#         self.stats_db: dict[str, list[dict[str, str | float]]] = {}
#         self.timer: Timer = Timer(name="rand_val_time")
#         self.value: tuple[int, int] = (0, 0)
#         self.train_values: list[tuple[int, int]] = []
#         self.prev_idx: int = -1
#
#     def next(self) -> tuple[int, int]:
#         self.timer.start()
#         self.value = (randint(1, 9), randint(1, 9))
#         return self.value
#
#     def done(self) -> None:
#         if self.value != (0, 0):
#             self.measured_times[self.timer.duration()] = self.value
#
#     def session_stats(self) -> dict[str, str | float]:
#         if not self._session_stats:
#             sum = 0
#             max = 0
#             min = 100
#             for t in self.measured_times.keys():
#                 sum += t
#                 if t > max:
#                     max = t
#                 if t < min:
#                     min = t
#
#             avg = sum / len(self.measured_times)
#
#             self._session_stats = {
#                 "date": str(datetime.now()),
#                 "avg": float(f"{avg:.2f}"),
#                 "max": float(f"{max:.2f}"),
#                 "min": float(f"{min:.2f}"),
#             }
#         return self._session_stats
#
#     def stats(self) -> dict[str, list[dict[str, str | float]]]:
#         if not self.stats_db:
#             data = self.load_db()
#             _ = data.setdefault("stats", [])
#             data["stats"].append(self._session_stats)
#             self.stats_db = data
#
#         return self.stats_db
#
#     def load_db(self) -> dict[str, list[dict[str, str | float]]]:
#         db_file = Path("stats.json")
#         data: dict[str, list[dict[str, str | float]]] = {}
#         if db_file.is_file():
#             with open("stats.json") as stats:
#                 data = json.load(stats)
#
#         return data
#
#     def save_stats(self) -> None:
#         with open("stats.json", "w") as stats:
#             json.dump(self.stats(), stats)
#
#     @property
#     def num_train_values(self) -> int:
#         return round(len(self.measured_times) * RandValStats.SELECTION_FRACTION)
#
#     def sorted(self) -> dict[float, tuple[int, int]]:
#         return dict(sorted(self.measured_times.items()))
#
#     @method_cache
#     def slowest_n_percent_values(self) -> list[tuple[int, int]]:
#         data = list(self.sorted().values())[-self.num_train_values :]
#         return data
#
#     def next_train_val(self) -> tuple[int, int]:
#         idx = randint(0, len(self.slowest_n_percent_values()) - 1)
#         while idx == self.prev_idx:
#             idx = randint(0, len(self.slowest_n_percent_values()) - 1)
#
#         self.prev_idx = idx
#         return self.slowest_n_percent_values()[idx]
