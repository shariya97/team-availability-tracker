import sqlite3
from datetime import datetime

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS team_members")

cursor.execute("""
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    available INTEGER DEFAULT 1,
    last_updated TEXT,
    available_at TEXT
)
""")

now = datetime.now().isoformat()

cursor.executemany(
    """
    INSERT INTO team_members
    (name, role, available, last_updated, available_at)
    VALUES (?, ?, ?, ?, ?)
    """,
    [
        ("Alex Rivers", "Senior Developer", 1, now, None),
        ("Samantha Chen", "UX Designer", 0, now, None),
        ("Jordan Taylor", "Project Manager", 1, now, None),
        ("Maria Garcia", "Marketing Lead", 0, now, None)
    ]
)

conn.commit()
conn.close()

print("Database created")