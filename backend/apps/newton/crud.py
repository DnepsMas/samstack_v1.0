import sqlite3, os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password_hash TEXT, memos_user_id TEXT, current_conv_id TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                     id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,
                     conversation_id TEXT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

def get_user(username: str):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        return c.fetchone()

def save_message(username: str, conv_id: str, role: str, content: str):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (username, conversation_id, role, content) VALUES (?, ?, ?, ?)", 
                  (username, conv_id, 'user' if role=='user' else 'assistant', content))

def get_history(username: str, conv_id: str, limit: int = 10):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT role, content FROM chat_history WHERE username=? AND conversation_id=? ORDER BY id DESC LIMIT ?", 
                  (username, conv_id, limit))
        rows = c.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

init_db()