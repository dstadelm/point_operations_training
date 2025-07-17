from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class SelectUserState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        self.presenter.view.show_user_selection(self.presenter.users, self._set_user)

    def _set_user(self, value: str | None):
        if not value:
            self.presenter.switch_to_create_user_state()
        else:
            self.presenter.user_name = value
            self.presenter.switch_to_welcome_state()

    def home(self) -> None:
        """Initialize the presenter and switch to WelcomeState."""
        self.presenter.switch_to_welcome_state()

    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def start_assignments(self) -> None: ...
    def create_user(self) -> None: ...
    def stats(self) -> None: ...

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
