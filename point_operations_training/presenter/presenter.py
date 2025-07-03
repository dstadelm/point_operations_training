from __future__ import annotations

from pathlib import Path

from point_operations_training.model.assignment import (
    AssignmentFactory,
    MultiplicationAssignmentFactory,
)
from point_operations_training.model.data_base import DataBase
from point_operations_training.model.session import Session
from point_operations_training.model.user import User, UserCollection
from point_operations_training.presenter.assignment_state import AssignmentsState
from point_operations_training.presenter.create_new_user_state import CreateNewUserState
from point_operations_training.presenter.init_state import InitState
from point_operations_training.presenter.select_modus_state import SelectModusState
from point_operations_training.presenter.select_user_state import SelectUserState
from point_operations_training.presenter.state import State
from point_operations_training.presenter.welcome_state import WelcomeState
from point_operations_training.view.view import UserView


class Presenter:

    def __init__(self) -> None:
        self._db_path: Path = Path("db.json")
        self._db: DataBase = DataBase(self._db_path)
        # if not self._db_path.exists():
        #     self._db.create_empty_db()
        #
        self._user_collection: UserCollection = self._db.get_user_collection()
        self._user_name: str = self._db.get_user_collection().last_user
        self._modus_operandi: AssignmentFactory = MultiplicationAssignmentFactory()
        self._session: Session = Session(self._modus_operandi)
        self._view: UserView = UserView()
        self.install_view_hooks()
        self._state: State = InitState(self)

        self._num_assignments: int = 20
        self._num_training: int = 20

    @property
    def num_assignments(self) -> int:
        return self._num_assignments

    @property
    def num_training(self) -> int:
        return self._num_training

    @property
    def session(self) -> Session:
        return self._session

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        self._state = new_state

    @property
    def view(self) -> UserView:
        return self._view

    @property
    def modus_operandi(self) -> AssignmentFactory:
        return self._modus_operandi

    @modus_operandi.setter
    def modus_operandi(self, value: AssignmentFactory) -> None:
        self._modus_operandi = value
        self._session = Session(self._modus_operandi)

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, name: str) -> None:
        if name not in self.users:
            new_user = User(name)
            self._user_collection.add_user(new_user)
        if name not in self.users:
            raise ValueError(f"User '{name}' does not exist.")
        self._user_name = name

    @property
    def users(self) -> list[str]:
        """Returns a list of user names."""
        return [user.name for user in self._user_collection.users]

    def commit_assignment(self) -> None:
        self._session.commit_assignment()

    def switch_to_create_user_state(self) -> None:
        self.state = CreateNewUserState(self)

    def switch_to_welcome_state(self) -> None:
        self.state = WelcomeState(self)

    def switch_to_select_user_state(self) -> None:
        self.state = SelectUserState(self)

    def switch_to_select_modus_state(self) -> None:
        self.state = SelectModusState(self)

    def switcht_to_assignment_state(self) -> None:
        self.state = AssignmentsState(self)

    def run(self) -> None:
        _ = self._view.run()  # pyright: ignore [reportUnknownVariableType]

    #########################################################
    # From here onwards functions that are hooks for the view
    #

    def install_view_hooks(self) -> None:
        self._view.on_select_user = self.select_user
        self._view.on_select_modi_operandi = self.select_modi_operandi
        self._view.on_start_assignments = self.start_assignments
        self._view.on_create_user = self.create_user
        self._view.on_home = self.home

    def select_user(self) -> None:
        if callable(self.state.select_user):
            self.state.select_user()

    def select_modi_operandi(self) -> None:
        if callable(self.state.select_modi_operandi):
            self.state.select_modi_operandi()

    def start_assignments(self) -> None:
        if callable(self.state.start_assignments):
            self.state.start_assignments()

    def create_user(self) -> None:
        if callable(self.state.create_user):
            self.state.create_user()

    def home(self) -> None:
        if callable(self.state.home):
            self.state.home()
