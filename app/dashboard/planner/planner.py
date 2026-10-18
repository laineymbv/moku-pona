from flask import request, redirect, url_for, Blueprint
import sqlite3
from app.dashboard.config import DB_FILE

api = Blueprint('planner', __name__)


@api.route("/add_plan", methods=["POST"])
# Sends plan data to DB
def submit_plan():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    meal_name_received = request.form.get("meal_name")
    meal_date_received = request.form.get("meal_date")
    meal_time_received = request.form.get("meal_time")
    meal_calories_received = request.form.get("meal_calories")
    if meal_name_received and meal_date_received and meal_time_received:
            cur.execute("INSERT INTO planned_meals (meal_name, meal_date, meal_time, meal_calories) VALUES (?, ?, ?, ?)", (meal_name_received, meal_date_received, meal_time_received, meal_calories_received))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for('dashboard.index'))
    cur.close()
    con.close()
    return "Error: Missing form entries", 400
@api.route("/toggle_eaten/<int:plan_id>", methods=["POST"])
# Toggles marker for if a meal is eaten
def toggle_eaten(plan_id):
    is_eaten = 1 if request.form.get("is_meal_eaten") else 0
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("UPDATE planned_meals SET is_meal_eaten = ? WHERE id = ?", (is_eaten, plan_id))
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('dashboard.index'))
# Adds calories from a meal to the total for the day
def add_calories_to_day(meal_date, meal_calories):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("UPDATE days SET calories_eaten = calories_eaten + ? WHERE day_date = ?", (meal_calories, meal_date))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO days (day_date, calories_eaten) VALUES (?, ?)", (meal_date, meal_calories))
    con.commit()
    cur.close()
    con.close()