import sqlite3
import os
from app.db import init_db
from app.dashboard.config import DB_FILE
from app.dashboard.routes import dashboard_bp
from app.dashboard.planner.planner import api
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
init_db()
app.register_blueprint(dashboard_bp)
app.register_blueprint(api)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
