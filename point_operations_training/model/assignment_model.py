from pathlib import Path

from point_operations_training.model.data_base import DataBase
from point_operations_training.model.result import ResultCollection, result_from_session
from point_operations_training.model.session import Session
from point_operations_training.model.user import UserCollection
from point_operations_training.presenter.modus import Modus


class AssignmentModel:
    def __init__(self, data_base_file: Path):
        self._db: DataBase = DataBase(data_base_file)
        self._user_collection: UserCollection = self._db.get_user_collection()
        self._session: Session | None = None
        self._modus: Modus = Modus.MULTIPLICATION

    @property
    def users(self) -> list[str]:
        """Returns a list of user names."""
        return [user.name for user in self._user_collection.users]

    @property
    def user(self) -> str:
        return (
            self._user_collection.current_user.name
            if self._user_collection.current_user
            else ""
        )

    @user.setter
    def user(self, user_name: str) -> None:
        if user_name not in self.users:
            self._user_collection.create_new_user(user_name)
        if user_name not in self.users:
            raise ValueError(f"User '{user_name}' does not exist.")
        self._user_collection.set_current_user(user_name)

    @property
    def modus(self) -> Modus:
        """Returns the current modus."""
        return self._modus

    @modus.setter
    def modus(self, modus: Modus) -> None:
        self._modus = modus

    def start_session(self) -> None:
        """Starts a new session for the current user with the given modus."""
        if not self._user_collection.current_user:
            raise ValueError("No current user set.")
        self._session = Session(self._user_collection.current_user.name, self._modus)

    def get_new_assignment(self) -> str:
        """Returns a new assignment for the current session."""
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.get_new_assignment()

    def get_next_train_assignment(self) -> str:
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.get_next_train_assignement()

    def commit_assignment(self) -> None:
        """Commits the current assignment in the session."""
        if not self._session:
            raise ValueError("Session not started.")
        self._session.commit_assignment()

    def get_solved_progress(self) -> tuple[int, int]:
        """Returns the number of solved assignments in the current session."""
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.get_solved_progress()

    def get_training_progress(self) -> tuple[int, int]:
        """Returns the number of solved training assignments in the current session."""
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.get_training_progress()

    def save_session(self) -> None:
        """Saves the current session to the database."""
        if not self._session:
            raise ValueError("Session not started.")
        self._db.save_db(self._user_collection)
        user = self._user_collection.current_user
        result = result_from_session(self._session)

        if user:
            user.add_result(str(self._modus.value), result)
            user.get_max_matrix(str(self._modus.value)).update(self._session)
            self._db.save_db(self._user_collection)

    def session_min(self) -> float:
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.min

    def session_max(self) -> float:
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.max

    def session_avg(self) -> float:
        if not self._session:
            raise ValueError("Session not started.")
        return self._session.avg

    def get_results(self) -> ResultCollection:
        if self._user_collection.current_user:
            return self._user_collection.current_user.get_results(
                str(self._modus.value)
            )
        else:
            return ResultCollection()
