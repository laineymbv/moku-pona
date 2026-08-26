import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "mealtracker.db")
# Initializes the DB
def init_db():
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT NOT NULL,
            meal_date TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS planned_meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_date TEXT NOT NULL,
            meal_name TEXT NOT NULL,
            meal_time TEXT NOT NULL,
            is_meal_eaten INTEGER
        )
    ''')
    con.commit()
    con.close()

init_db()

@app.route("/", methods=["GET", "POST"])
# Runs the website
def index():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT id, meal_name, meal_date, meal_time, is_meal_eaten FROM planned_meals")
    all_plans = cur.fetchall()
    cur.close()
    con.close()
    return render_template("index.html", planned_meals=all_plans)
@app.route("/add_plan", methods=["POST"])
# Sends plan data to DB
def submit_plan():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    meal_name_received = request.form.get("meal_name")
    meal_date_received = request.form.get("meal_date")
    meal_time_received = request.form.get("meal_time")
    if meal_name_received and meal_date_received and meal_time_received:
            cur.execute("INSERT INTO planned_meals (meal_name, meal_date, meal_time) VALUES (?, ?, ?)", (meal_name_received, meal_date_received, meal_time_received))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for('index'))
    cur.close
    con.close
    return "Error: Missing form entries", 400
@app.route("/toggle_eaten/<int:plan_id>", methods=["POST"])
# Toggles if a meal is eaten
def toggle_eaten(plan_id):
    is_eaten = 1 if request.form.get("is_meal_eaten") else 0
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("UPDATE planned_meals SET is_meal_eaten = ? WHERE id = ?", (is_eaten, plan_id))
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
