from typing import Callable, Protocol

from point_operations_training.model.result import ResultCollectionProtocol
from point_operations_training.presenter.modus import Modus


class View(Protocol):

    on_select_user: Callable[..., None]
    on_select_modi_operandi: Callable[..., None]
    on_start_assignments: Callable[..., None]
    on_create_user: Callable[..., None]
    on_home: Callable[..., None]
    on_stats: Callable[..., None]

    def show_welcome_screen(self, name: str, modus: str) -> None: ...

    def show_assignment_screen(
        self,
        user: str,
        assignment: str,
        total_assignments: int,
        solved_assignments: int,
    ) -> None: ...

    def show_user_selection(
        self, users: list[str], callback: Callable[[str | None], None]
    ) -> None: ...

    def show_create_new_user(
        self, users: list[str], callback: Callable[[str | None], None]
    ) -> None: ...

    def show_modus_selection(
        self, callback: Callable[[Modus | None], None]
    ) -> None: ...

    def show_result_screen(self, results: str) -> None: ...

    def show_stats_screen(self, results: ResultCollectionProtocol) -> None: ...

    def run(self) -> None: ...
