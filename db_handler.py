# db_handler.py
import sqlite3
import os

home_dir = os.path.expanduser("~")
APP_DATA_DIR = os.path.join(home_dir, ".organizador_de_times")
os.makedirs(APP_DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(APP_DATA_DIR, "organizador.db")
print(f"Usando banco de dados em: {DB_PATH}")

def execute_migrations():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, skill INTEGER, photo_path TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS lists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS list_players (
                list_id INTEGER, player_id INTEGER,
                FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
                FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
                PRIMARY KEY (list_id, player_id)
            )""")
        cursor.execute("SELECT count(*) FROM lists")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO lists (name) VALUES (?)", ('Jogadores Gerais',))
            print("Lista padrão 'Jogadores Gerais' criada.")
        conn.commit()

def create_list(name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lists (name) VALUES (?)", (name,))
        return cursor.lastrowid

def get_all_lists():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT id, name FROM lists ORDER BY name COLLATE NOCASE ASC").fetchall()

def get_list_name(list_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT name FROM lists WHERE id = ?", (list_id,)).fetchone()
        return result[0] if result else ""

def get_list_by_name(name):
    """Busca uma lista pelo nome e retorna seus dados se existir."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name FROM lists WHERE name COLLATE NOCASE = ?"
        return conn.execute(query, (name,)).fetchone()

def get_all_player_list_associations():
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT p.id, p.name, p.skill, p.photo_path, l.name as list_name
            FROM players p
            JOIN list_players lp ON p.id = lp.player_id
            JOIN lists l ON l.id = lp.list_id
            ORDER BY l.name, p.name COLLATE NOCASE
        """
        return conn.execute(query).fetchall()

def rename_list(list_id, new_name):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE lists SET name = ? WHERE id = ?", (new_name, list_id))

def delete_list(list_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM lists WHERE id = ?", (list_id,))
        conn.execute("DELETE FROM list_players WHERE list_id = ?", (list_id,))

def add_player_to_list(list_id, player_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT OR IGNORE INTO list_players (list_id, player_id) VALUES (?, ?)", (list_id, player_id))

def get_players_by_list(list_id):
    if not list_id: return []
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT p.id, p.name, p.skill, p.photo_path FROM players p JOIN list_players lp ON p.id = lp.player_id WHERE lp.list_id = ? ORDER BY p.name COLLATE NOCASE ASC"
        return conn.execute(query, (list_id,)).fetchall()

def get_all_players():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name, skill, photo_path FROM players ORDER BY name COLLATE NOCASE ASC"
        return conn.execute(query).fetchall()

def get_player_by_name(name):
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name, skill, photo_path FROM players WHERE name COLLATE NOCASE = ?"
        return conn.execute(query, (name,)).fetchone()

def insert_player(name, skill, photo_path=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (name, skill, photo_path) VALUES (?, ?, ?)", (name, skill, photo_path))
        return cursor.lastrowid

def delete_player(player_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM players WHERE id = ?", (player_id,))
        conn.execute("DELETE FROM list_players WHERE player_id = ?", (player_id,))

def update_player(player_id, name, skill, photo_path=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE players SET name = ?, skill = ?, photo_path = ? WHERE id = ?", (name, skill, photo_path, player_id))

def update_players_in_list(list_id, new_player_ids):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM list_players WHERE list_id = ?", (list_id,))
        if new_player_ids:
            values_to_insert = [(list_id, player_id) for player_id in new_player_ids]
            conn.executemany("INSERT INTO list_players (list_id, player_id) VALUES (?, ?)", values_to_insert)