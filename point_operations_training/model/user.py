from point_operations_training.model.max_matrix import MaxMatrix, MaxMatrixType
from point_operations_training.model.result import (
    Result,
    ResultCollection,
    ResultCollectionType,
)

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
        self._current_user: User | None = None

    def to_dict(self) -> UserCollectionType:
        if self._current_user is None:
            raise ValueError("No current user set.")
        data: UserCollectionType = {"last_user": self._current_user.name, "users": {}}
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
        last_user: str = data.get(
            "last_user", ""
        )  # pyright: ignore [reportAssignmentType]

        self._current_user = self.get_user(last_user)

    def get_users(self) -> list[str]:
        return [u.name for u in self.users]

    def create_new_user(self, user_name: str) -> None:
        self._current_user = User(user_name)
        self.users.append(self._current_user)

    def get_user(self, name: str) -> User | None:
        for user in self.users:
            if user.name == name:
                return user

    @property
    def current_user(self) -> User | None:
        return self._current_user

    def set_current_user(self, user_name: str) -> None:
        self._current_user = self.get_user(user_name)
