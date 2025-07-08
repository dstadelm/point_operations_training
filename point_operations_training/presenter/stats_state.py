from typing import override

from point_operations_training.presenter.presenter_protocol import PresenterProtocol


class StatsState:
    def __init__(self, presenter: PresenterProtocol) -> None:
        self.presenter: PresenterProtocol = presenter
        user = self.presenter.user_collection.get_user(self.presenter.user_name)
        results = None
        if user:
            results = user.get_results(str(self.presenter.modus.value))

        if results:
            self.presenter.view.show_stats_screen(results)
        else:
            self.presenter.switch_to_welcome_state()

    def start_assignments(self) -> None: ...
    def select_user(self) -> None: ...
    def select_modi_operandi(self) -> None: ...
    def create_user(self) -> None: ...
    def home(self) -> None:
        self.presenter.switch_to_welcome_state()

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
