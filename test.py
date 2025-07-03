from pathlib import Path

from point_operations_training.training_set import DataBase

if __name__ == "__main__":
    db = DataBase(Path("db.json"))
    users = db.get_user_collection()
    print(users.get_users())
    user = users.get_user("testuser")
    print(user.results["*"])
