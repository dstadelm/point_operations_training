import json
from pathlib import Path

from point_operations_training.model.user import UserCollection, UserCollectionType

DataBaseType = dict[str, UserCollectionType | str]


class DataBase:
    def __init__(self, file: Path) -> None:  # noqa: F821
        self.file: Path = file
        self.data: DataBaseType = {}

    def get_db(self) -> DataBaseType:
        if not self.data:
            if self.file.is_file():
                with open(self.file) as stats:
                    self.data = json.load(stats)

        return self.data

    def save_db(self, data: UserCollection) -> None:
        with open(self.file, "w") as stats:
            json.dump(data.to_dict(), stats)

    def get_user_collection(self) -> UserCollection:
        data = self.get_db()
        users = UserCollection()
        users.from_dict(data)  # pyright: ignore [reportArgumentType]
        return users
