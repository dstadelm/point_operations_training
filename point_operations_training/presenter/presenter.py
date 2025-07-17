from __future__ import annotations

from point_operations_training.model.model import Model
from point_operations_training.presenter.assignment_state import AssignmentsState
from point_operations_training.presenter.create_new_user_state import CreateNewUserState
from point_operations_training.presenter.init_state import InitState
from point_operations_training.presenter.modus import Modus
from point_operations_training.presenter.result_state import ResultState
from point_operations_training.presenter.select_modus_state import SelectModusState
from point_operations_training.presenter.select_user_state import SelectUserState
from point_operations_training.presenter.state import State
from point_operations_training.presenter.stats_state import StatsState
from point_operations_training.presenter.training_state import TrainingState
from point_operations_training.presenter.welcome_state import WelcomeState
from point_operations_training.view.view_protocol import ViewProtocol


class Presenter:

    def __init__(self, view: ViewProtocol, model: Model) -> None:
        self._model: Model = model
        self._view: ViewProtocol = view
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
    def view(self) -> ViewProtocol:
        return self._view

    @property
    def model(self) -> Model:
        return self._model

    @property
    def modus(self) -> Modus:
        return self._model.modus

    @modus.setter
    def modus(self, value: Modus) -> None:
        self._model.modus = value

    @property
    def user_name(self) -> str:
        return self._model.user

    @user_name.setter
    def user_name(self, name: str) -> None:
        self._model.user = name

    @property
    def users(self) -> list[str]:
        """Returns a list of user names."""
        return self._model.users

    def switch_to_create_user_state(self) -> None:
        self._state = CreateNewUserState(self)

    def switch_to_welcome_state(self) -> None:
        self._state = WelcomeState(self)

    def switch_to_select_user_state(self) -> None:
        self._state = SelectUserState(self)

    def switch_to_select_modus_state(self) -> None:
        self._state = SelectModusState(self)

    def switch_to_assignment_state(self) -> None:
        self._state = AssignmentsState(self)

    def switch_to_result_state(self) -> None:
        self._state = ResultState(self)

    def switch_to_training_state(self) -> None:
        self._state = TrainingState(self)

    def switch_to_stats_state(self) -> None:
        self._state = StatsState(self)

    def run(self) -> None:
        _ = self._view.run()

    #########################################################
    # From here onwards functions that are hooks for the view
    #

    def install_view_hooks(self) -> None:
        self._view.on_select_user = self.select_user
        self._view.on_select_modi_operandi = self.select_modi_operandi
        self._view.on_start_assignments = self.start_assignments
        self._view.on_create_user = self.create_user
        self._view.on_home = self.home
        self._view.on_stats = self.stats

    def select_user(self) -> None:
        if callable(self._state.select_user):
            self._state.select_user()

    def select_modi_operandi(self) -> None:
        if callable(self._state.select_modi_operandi):
            self._state.select_modi_operandi()

    def start_assignments(self) -> None:
        if callable(self._state.start_assignments):
            self._state.start_assignments()

    def create_user(self) -> None:
        if callable(self._state.create_user):
            self._state.create_user()

    def home(self) -> None:
        if callable(self._state.home):
            self._state.home()

    def stats(self) -> None:
        if callable(self._state.stats):
            self._state.stats()
