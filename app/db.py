import os
import sqlite3

from app.dashboard.config import DB_FILE

# Initializes the DB
def init_db():
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS planned_meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_date TEXT NOT NULL,
            meal_name TEXT NOT NULL,
            meal_time TEXT NOT NULL,
            is_meal_eaten INTEGER,
            meal_calories INTEGER,
            day TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()