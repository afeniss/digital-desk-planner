from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta
import sqlite3

app = Flask(__name__)

DATABASE = "planner.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_planner (
            planner_date TEXT PRIMARY KEY,
            priority1 TEXT,
            priority2 TEXT,
            priority3 TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    today = date.today()
    yesterday = today - timedelta(days=1)
    today_str = today.isoformat()

    conn = get_db()

    if request.method == "POST":
        priority1 = request.form.get("priority1", "")
        priority2 = request.form.get("priority2", "")
        priority3 = request.form.get("priority3", "")
        notes = request.form.get("notes", "")

        conn.execute("""
            INSERT INTO daily_planner
            (planner_date, priority1, priority2, priority3, notes)
            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(planner_date)
            DO UPDATE SET
                priority1 = excluded.priority1,
                priority2 = excluded.priority2,
                priority3 = excluded.priority3,
                notes = excluded.notes
        """, (
            today_str,
            priority1,
            priority2,
            priority3,
            notes
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    row = conn.execute(
        "SELECT * FROM daily_planner WHERE planner_date = ?",
        (today_str,)
    ).fetchone()

    conn.close()

    return render_template(
        "index.html",
        today=today,
        yesterday=yesterday,
        planner=row
    )


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )