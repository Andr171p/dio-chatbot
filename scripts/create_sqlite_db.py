import sqlite3

from src.settings import BASE_DIR


db_path = BASE_DIR / "db.sqlite3"


connection = sqlite3.connect(db_path)
