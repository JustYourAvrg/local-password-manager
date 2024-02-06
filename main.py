import database

from manager import Manager


if __name__ == "__main__":
    database.setting_up_db()
    Manager()
