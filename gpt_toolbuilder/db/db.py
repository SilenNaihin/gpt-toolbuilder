import json
import time
from typing import Any

from gpt_toolbuilder.utils.Singleton import Singleton


class Database(metaclass=Singleton):
    def initialize(self, db_file):
        # Moved initialization logic here
        self.db_file = db_file
        self.load_db()

    def load_db(self):
        try:
            with open(self.db_file, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        with open(self.db_file, "w") as f:
            json.dump(self.db, f, indent=4)

    @classmethod
    def add_entry(cls, type: str, data: Any):
        # Use the instance stored at class level
        instance = cls.instance

        assert hasattr(
            instance, "db_file"
        ), "Database is not initialized yet, call Database().initialize('db_file') first"

        entry = {"type": type, "data": data}
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        instance.db[timestamp] = entry
        instance.save_db()  # save the database after adding each entry
