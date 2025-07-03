# presenter.py

from model import UserModel
from view import UserView


class UserPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Attach event handlers
        self.view.on_user_list_request = self.handle_user_list_request
        self.view.on_user_select = self.handle_user_selection

    def handle_user_list_request(self):
        users = self.get_users()
        self.view.show_users(users)

    def handle_user_selection(self, index):
        user = self.get_user_info(index)
        self.view.show_user_birthday(user)

    def get_users(self):
        return self.model.users

    def get_user_info(self, index):
        return self.model.users[index - 1]  # 1-based to 0-based index

    def run(self):
        self.view.run()


if __name__ == "__main__":
    model = UserModel("users.json")
    view = UserView()
    presenter = UserPresenter(model, view)
    presenter.run()
