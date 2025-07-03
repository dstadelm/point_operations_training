# model.py

import json


class UserModel:
    def __init__(self, json_file):
        self.users = self.load_data(json_file)

    def load_data(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
        return data.get("users", [])
