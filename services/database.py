import sqlite3
from config import DB_FILE

def init_db():
    """Initialize SQLite database."""
    with sqlite3.connect(DB_FILE) as conn:
        # conn.execute("DROP TABLE IF EXISTS reminders")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                chat_id INTEGER NOT NULL,
                cron_expr TEXT NOT NULL,
                last_run TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, symbol)
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, symbol)
            )
        """
        )
        conn.commit()

def add_reminder(chat_id, symbol, cron_expr):
    """Menambahkan pengingat ke database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO reminders (chat_id, symbol, cron_expr, last_run) VALUES (?, ?, ?, NULL)",
            (chat_id, symbol, cron_expr)
        )
        conn.commit()

def get_reminders(chat_id=None):
    """Mengambil semua reminder atau reminder berdasarkan chat_id."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        if chat_id:
            cursor.execute("SELECT chat_id, symbol, cron_expr FROM reminders WHERE chat_id = ?", (chat_id,))
        else:
            cursor.execute("SELECT chat_id, symbol, cron_expr FROM reminders")
        return cursor.fetchall()

def remove_reminder(chat_id, symbol):
    """Menghapus reminder berdasarkan chat_id dan symbol, serta mengembalikan status keberhasilan."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
        conn.commit()
        return cursor.rowcount > 0

def add_watchlist(chat_id, symbols):
    """Menambahkan simbol ke watchlist untuk chat_id tertentu."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        for symbol in symbols:
            cursor.execute("INSERT OR IGNORE INTO watchlist (chat_id, symbol) VALUES (?, ?)", (chat_id, symbol.upper()))
        conn.commit()

def remove_watchlist(chat_id, symbol):
    """Menghapus koin dari watchlist pengguna."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watchlist WHERE chat_id = ? AND symbol = ?", (chat_id, symbol))
        conn.commit()

def get_watchlist(chat_id):
    """Mengambil watchlist berdasarkan chat_id."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM watchlist WHERE chat_id = ?", (chat_id,))
        symbols = [row[0] for row in cursor.fetchall()]
    return symbols
