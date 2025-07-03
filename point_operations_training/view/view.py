from typing import Callable

from textual.app import App, ComposeResult, ScreenStackError

# from textual.reactive import reactive
from textual.containers import Center
from textual.widgets import Footer, Header, Label

from point_operations_training.model.assignment import AssignmentFactory
from point_operations_training.presenter.empty_hook import create_empty_event_hook
from point_operations_training.view.assignment_screen import AssignmentScreen
from point_operations_training.view.create_new_user_screen import CreateNewUser
from point_operations_training.view.quit_screen import QuitScreen
from point_operations_training.view.select_modus_screen import SelectModus
from point_operations_training.view.select_user_screen import UserSelectionScreen
from point_operations_training.view.welcome_screen import WelcomeScreen


class UserView(App):  # pyright: ignore [reportMissingTypeArgument]
    CSS_PATH = "view.tcss"  # pyright: ignore [reportUnannotatedClassAttribute]
    BINDINGS = [  # pyright: ignore [reportUnannotatedClassAttribute]
        ("enter", "new_assignment", "New Assignment"),
        ("escape", "home", "Home"),
        ("u", "select_user", "Select user"),
        ("o", "select_modi_operandi", "Select operation"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.on_select_user: Callable[..., None] = create_empty_event_hook(
            "on_select_user event"
        )  # Event hook for user selection
        self.on_select_modi_operandi: Callable[..., None] = create_empty_event_hook(
            "on_select_modi_operandi"
        )  # Event hook to request user list
        self.on_start_assignments: Callable[..., None] = create_empty_event_hook(
            "on_start_assignements"
        )  # Event hook to start assignments
        self.on_create_user: Callable[..., None] = create_empty_event_hook(
            "on_create_user"
        )
        #
        self.on_home: Callable[..., None] = create_empty_event_hook(
            event_hook_name="on_initialize"
        )  # Event hook to initialize the app

    def compose(self) -> ComposeResult:  # pyright: ignore [reportImplicitOverride]
        """Called to add widgets to the app."""
        yield Header()

        with Center():
            yield Label("Press ENTER to start!", id="start")

        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.on_home()

    def clear(self) -> None:
        """Clear the screen stack."""
        try:
            _ = self.pop_screen()
        except ScreenStackError:
            pass

    def show_welcome_screen(self, name: str) -> None:
        """Show the welcome screen."""
        self.clear()
        _ = self.push_screen(WelcomeScreen(name))

    def show_assignment_screen(
        self,
        user: str,
        assignment: str,
        total_assignments: int,
        solved_assignments: int,
    ) -> None:
        """Show the assignment screen."""
        self.clear()
        _ = self.push_screen(
            AssignmentScreen(
                user=user,
                assignement=assignment,
                total_assignments=total_assignments,
                solved_assignments=solved_assignments,
            )
        )

    def show_user_selection(
        self, users: list[str], callback: Callable[[str | None], None]
    ) -> None:
        self.clear()
        _ = self.push_screen(UserSelectionScreen(users), callback=callback)

    def show_create_new_user(
        self, users: list[str], callback: Callable[[str | None], None]
    ) -> None:
        self.clear()
        _ = self.push_screen(CreateNewUser(users), callback=callback)

    def show_modi_operandi_selection(
        self, callback: Callable[[AssignmentFactory | None], None]
    ) -> None:
        self.clear()
        _ = self.push_screen(SelectModus(), callback=callback)

    def action_start_assignements(self) -> None:
        self.on_start_assignments()

    def action_request_quit(self) -> None:
        _ = self.push_screen(QuitScreen())

    def action_select_user(self) -> None:
        self.on_select_user()

    def action_select_modi_operandi(self) -> None:
        self.on_select_modi_operandi()

    def action_new_assignment(self) -> None:
        self.on_start_assignments()

    def action_home(self) -> None:
        self.on_home()
