from flask import Flask, render_template, redirect
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def time_ago(timestamp):

    if not timestamp:
        return "Unknown"

    dt = datetime.fromisoformat(timestamp)

    diff = datetime.now() - dt

    mins = int(diff.total_seconds() / 60)

    if mins < 60:
        return f"{mins} mins ago"

    hours = mins // 60

    return f"{hours} hrs ago"


def available_in(timestamp):

    if not timestamp:
        return None

    dt = datetime.fromisoformat(timestamp)

    diff = dt - datetime.now()

    mins = int(diff.total_seconds() / 60)

    if mins <= 0:
        return "Now"

    if mins < 60:
        return f"{mins} mins"

    hours = mins // 60

    return f"{hours} hr(s)"


@app.route("/")
def index():

    conn = get_db()

    members = conn.execute(
        "SELECT * FROM team_members"
    ).fetchall()

    member_list = []

    for member in members:

        member = dict(member)

        member["time_ago"] = time_ago(
            member["last_updated"]
        )

        member["available_in"] = available_in(
            member["available_at"]
        )

        member_list.append(member)

    conn.close()

    return render_template(
        "index.html",
        members=member_list
    )


@app.route("/toggle/<int:id>", methods=["POST"])
def toggle(id):

    conn = get_db()

    member = conn.execute(
        "SELECT * FROM team_members WHERE id=?",
        (id,)
    ).fetchone()

    conn.execute(
        """
        UPDATE team_members
        SET available=1,
            last_updated=?,
            available_at=NULL
        WHERE id=?
        """,
        (
            datetime.now().isoformat(),
            id
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/set_busy/<int:id>/<int:hours>", methods=["POST"])
def set_busy(id, hours):

    conn = get_db()

    now = datetime.now()

    available_at = now + timedelta(hours=hours)

    conn.execute(
        """
        UPDATE team_members
        SET available=0,
            last_updated=?,
            available_at=?
        WHERE id=?
        """,
        (
            now.isoformat(),
            available_at.isoformat(),
            id
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)