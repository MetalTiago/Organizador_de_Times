
import sqlite3
import os

DB_PATH = os.path.join("db", "dbcad.db")
os.makedirs("db", exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)


def create_table():
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                skill INTEGER
            )
        """)


def insert_user(name, skill):
    with conn:
        conn.execute("INSERT INTO users (name, skill) VALUES (?, ?)", (name, skill))


def delete_user(user_id):
    with conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


def update_user(user_id, name, skill):
    with conn:
        conn.execute("UPDATE users SET name = ?, skill = ? WHERE id = ?", (name, skill, user_id))


def get_all_users():
    with conn:
        return conn.execute("SELECT * FROM users").fetchall()


def get_user_count():
    return len(get_all_users())
