# view.py

from textual.app import App


class UserView(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_user_select = None  # Event hook for user selection
        self.on_user_list_request = None  # Event hook to request user list
        self.current_selection = None

    async def on_mount(self) -> None:
        self.welcome_screen()

    def welcome_screen(self):
        self.clear()
        self.screen.print("Welcome to the User Birthday App!")
        self.screen.print("Press 'u' to view users.")

    async def handle_key(self, event) -> None:
        if event.key == "u" and self.on_user_list_request:
            self.on_user_list_request()

    def show_users(self, users):
        self.clear()
        self.screen.print("Select a user by number:")
        for index, user in enumerate(users):
            self.screen.print(f"{index + 1}. {user['name']}")

        # Capture user input for selection
        user_choice = int(input("Enter number to select user: "))
        if self.on_user_select:
            self.on_user_select(user_choice)

    def show_user_birthday(self, user):
        self.clear()
        self.screen.print(
            f"{user['name']}'s birthday is on {user['birthday']}. Press any key to go back."
        )
