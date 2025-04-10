import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "db.sqlite3"


if __name__ == "__main__":
    connection = sqlite3.connect(db_path)
