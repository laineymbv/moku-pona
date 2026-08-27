import sqlite3
from flask import render_template, Blueprint
dashboard_bp = Blueprint('dashboard', __name__)
from app.dashboard.config import DB_FILE

@dashboard_bp.route("/", methods=["GET", "POST"])
# Runs the website
def index():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT id, meal_name, meal_date, meal_time, is_meal_eaten FROM planned_meals")
    all_plans = cur.fetchall()
    cur.close()
    con.close()
    return render_template("index.html", planned_meals=all_plans)