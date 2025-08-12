from point_operations_training.model.max_matrix import MaxMatrix, MaxMatrixType
from point_operations_training.model.result import (
    Result,
    ResultCollection,
    ResultCollectionType,
)
from point_operations_training.presenter.modus import Modus

UserType = dict[str, dict[str, ResultCollectionType | MaxMatrixType] | str]


class User:
    def __init__(self, name: str = "") -> None:
        self.name: str = name
        self.results: dict[str, ResultCollection] = {}
        self.max_matrices: dict[str, MaxMatrix] = {}
        self.modus: Modus = Modus.MULTIPLICATION

    @property
    def max_matrix(self) -> MaxMatrix:
        return self.max_matrices.setdefault(str(self.modus.value), MaxMatrix())

    def avg_series(self) -> list[float]:
        return self.results[str(self.modus.value)].avg_series()

    def max_series(self) -> list[float]:
        return self.results[str(self.modus.value)].max_series()

    def min_series(self) -> list[float]:
        return self.results[str(self.modus.value)].min_series()

    def add_result(self, result: Result) -> None:
        self.results.setdefault(str(self.modus.value), ResultCollection()).add_result(
            result
        )

    def get_results(self) -> ResultCollection:
        if (str(self.modus.value)) in self.results:
            return self.results[str(self.modus.value)]
        return ResultCollection()

    def from_dict(
        self,
        data: UserType,
    ) -> None:
        for outer_key in data.keys():

            if outer_key == "last_modus":
                for m in Modus:
                    if str(m.value) == data[outer_key]:
                        self.modus = m

            else:
                # we have the results of a modus
                modus = data[outer_key]
                if isinstance(modus, dict):
                    for key, value in modus.items():
                        if key == "results":
                            self.results[outer_key] = ResultCollection()
                            self.results[outer_key].from_dict(
                                value  # pyright: ignore [reportArgumentType]
                            )
                        if key == "max_matrix":
                            self.max_matrices[outer_key] = MaxMatrix()
                            self.max_matrices[outer_key].matrix = (
                                value  # pyright: ignore [reportAttributeAccessIssue]
                            )

    def to_dict(self) -> UserType:
        data: UserType = {}
        data["last_modus"] = str(self.modus.value)
        for modus_operandi, result in self.results.items():
            data[modus_operandi] = {}
            data[modus_operandi][  # pyright: ignore [reportIndexIssue]
                "results"
            ] = result.to_dict()
            data[modus_operandi]["max_matrix"] = (  # pyright: ignore [reportIndexIssue]
                self.max_matrices[modus_operandi].matrix
            )

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
