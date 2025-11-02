# db_handler.py
import sqlite3
import os

# --- LÓGICA ORIGINAL RESTAURADA ---
# Esta lógica funciona no Desktop e é traduzida corretamente pelo Flet no Android
home_dir = os.path.expanduser("~")
APP_DATA_DIR = os.path.join(home_dir, ".organizador_de_times")
os.makedirs(APP_DATA_DIR, exist_ok=True) # Cria o diretório se não existir
DB_PATH = os.path.join(APP_DATA_DIR, "organizador.db")
print(f"Usando banco de dados em: {DB_PATH}")
# --- FIM DA RESTAURAÇÃO ---


def execute_migrations():
    """Garante que todas as tabelas e a lista padrão existam."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT COLLATE NOCASE,
                skill INTEGER,
                photo_path TEXT
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE COLLATE NOCASE
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS list_players (
                list_id INTEGER, player_id INTEGER,
                FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
                FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
                PRIMARY KEY (list_id, player_id)
            )""")
        # Garante que a tabela players tem a coluna photo_path (para migrações de versões antigas)
        try:
            cursor.execute("ALTER TABLE players ADD COLUMN photo_path TEXT")
            print("Coluna 'photo_path' adicionada à tabela 'players'.")
        except sqlite3.OperationalError:
            pass # Coluna já existe

        # Cria a lista padrão se nenhuma lista existir
        cursor.execute("SELECT count(*) FROM lists")
        if cursor.fetchone()[0] == 0:
            try:
                # O nome da lista padrão não deve ser traduzido no banco de dados
                cursor.execute("INSERT INTO lists (name) VALUES (?)", ('Jogadores Gerais',))
                print("Lista padrão 'Jogadores Gerais' criada.")
            except sqlite3.IntegrityError:
                 print("Lista padrão 'Jogadores Gerais' já existe.") # Caso raro
        conn.commit()

def create_list(name):
    """Cria uma nova lista e retorna seu ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO lists (name) VALUES (?)", (name,))
            conn.commit() # Commit após inserção
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Erro ao criar lista (possivelmente nome duplicado): {e}")
            raise e # Re-levanta a exceção para ser tratada na UI

def get_all_lists():
    """Retorna todas as listas (ID, Nome) ordenadas por nome."""
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT id, name FROM lists ORDER BY name COLLATE NOCASE ASC").fetchall()

def get_list_name(list_id):
    """Retorna o nome de uma lista específica pelo ID."""
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT name FROM lists WHERE id = ?", (list_id,)).fetchone()
        return result[0] if result else ""

def get_list_by_name(name):
    """Busca uma lista pelo nome e retorna seus dados (ID, Nome) se existir."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name FROM lists WHERE name COLLATE NOCASE = ?"
        return conn.execute(query, (name,)).fetchone()

def get_all_player_list_associations():
    """Retorna todas as associações jogador-lista para exportação."""
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT p.id, p.name, p.skill, p.photo_path, l.name as list_name
            FROM players p
            JOIN list_players lp ON p.id = lp.player_id
            JOIN lists l ON l.id = lp.list_id
            ORDER BY l.name COLLATE NOCASE, p.name COLLATE NOCASE
        """
        return conn.execute(query).fetchall()

def rename_list(list_id, new_name):
    """Renomeia uma lista existente."""
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("UPDATE lists SET name = ? WHERE id = ?", (new_name, list_id))
            conn.commit() # Commit após atualização
        except sqlite3.IntegrityError as e:
            print(f"Erro ao renomear lista (possivelmente nome duplicado): {e}")
            raise e # Re-levanta a exceção

def delete_list(list_id):
    """Deleta uma lista e suas associações com jogadores."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON") # Garante que ON DELETE CASCADE funcione
        conn.execute("DELETE FROM lists WHERE id = ?", (list_id,))
        conn.commit() # Commit após deleção

def add_player_to_list(list_id, player_id):
    """Adiciona um jogador a uma lista (ignora se já existe)."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT OR IGNORE INTO list_players (list_id, player_id) VALUES (?, ?)", (list_id, player_id))
        conn.commit() # Commit após inserção

def get_players_by_list(list_id):
    """Retorna os jogadores (ID, Nome, Skill, Foto) de uma lista específica."""
    if not isinstance(list_id, int) or list_id <= 0: return [] 
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT p.id, p.name, p.skill, p.photo_path
            FROM players p
            JOIN list_players lp ON p.id = lp.player_id
            WHERE lp.list_id = ?
            ORDER BY p.name COLLATE NOCASE ASC
            """
        return conn.execute(query, (list_id,)).fetchall()

def get_all_players():
    """Retorna todos os jogadores cadastrados (ID, Nome, Skill, Foto)."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name, skill, photo_path FROM players ORDER BY name COLLATE NOCASE ASC"
        return conn.execute(query).fetchall()

def get_player_by_name(name):
    """Busca um jogador pelo nome e retorna seus dados."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT id, name, skill, photo_path FROM players WHERE name COLLATE NOCASE = ?"
        return conn.execute(query, (name,)).fetchone()

def insert_player(name, skill, photo_path=None):
    """Insere um novo jogador e retorna seu ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (name, skill, photo_path) VALUES (?, ?, ?)", (name, skill, photo_path))
        conn.commit() # Commit após inserção
        return cursor.lastrowid

def delete_player(player_id):
    """Deleta um jogador e suas associações com listas."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON") # Garante ON DELETE CASCADE
        conn.execute("DELETE FROM players WHERE id = ?", (player_id,))
        conn.commit() # Commit após deleção

def update_player(player_id, name, skill, photo_path=None):
    """Atualiza os dados de um jogador existente."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE players SET name = ?, skill = ?, photo_path = ? WHERE id = ?", (name, skill, photo_path, player_id))
        conn.commit() # Commit após atualização

def update_players_in_list(list_id, new_player_ids):
    """Atualiza a lista de jogadores associados a uma lista específica."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM list_players WHERE list_id = ?", (list_id,))
        if new_player_ids:
            values_to_insert = [(list_id, player_id) for player_id in new_player_ids]
            conn.executemany("INSERT INTO list_players (list_id, player_id) VALUES (?, ?)", values_to_insert)
        conn.commit()

def count_custom_lists():
    """Conta o número de listas criadas pelo utilizador (exclui 'Jogadores Gerais')."""
    with sqlite3.connect(DB_PATH) as conn:
        try:
            result = conn.execute("SELECT COUNT(*) FROM lists WHERE name != 'Jogadores Gerais' COLLATE NOCASE").fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Erro ao contar listas personalizadas: {e}")
            return 999 

def count_all_players():
    """Conta o número total de jogadores cadastrados."""
    with sqlite3.connect(DB_PATH) as conn:
        try:
            result = conn.execute("SELECT COUNT(*) FROM players").fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Erro ao contar jogadores: {e}")
            return 0