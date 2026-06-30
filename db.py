import sqlite3

conn = sqlite3.connect("group_v3_ai.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    score INTEGER DEFAULT 100,
    risk INTEGER DEFAULT 0,
    warns INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    risk INTEGER,
    reason TEXT
)
""")

conn.commit()