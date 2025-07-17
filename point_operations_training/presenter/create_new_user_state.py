from typing import override

from point_operations_training.presenter.presenter import Presenter


class CreateNewUserState:
    def __init__(self, presenter: Presenter) -> None:
        self.presenter: Presenter = presenter
        self.presenter.view.show_create_new_user(self.presenter.users, self._add_user)

    def _add_user(self, name: str | None) -> None:
        if name:
            self.presenter.user_name = name
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
