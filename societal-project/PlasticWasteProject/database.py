import sqlite3
import os

# -----------------------------
# DATABASE PATH (LOCAL + RENDER SAFE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# If Render / cloud persistent disk is used
if os.path.exists("/data"):
    DB_PATH = "/data/database.db"


# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# -----------------------------
# INIT DATABASE
# -----------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plastic_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            recyclable TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Gracefully patch existing local DB schema with new Image Path column if it doesn't already exist
    try:
        cursor.execute("ALTER TABLE waste ADD COLUMN image_path TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass # Column already natively injected

    conn.commit()
    conn.close()


# -----------------------------
# INSERT DATA
# -----------------------------
def add_waste_log(plastic_type, quantity, recyclable):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO waste (plastic_type, quantity, recyclable)
            VALUES (?, ?, ?)
        """, (plastic_type, quantity, recyclable))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("DB Insert Error:", e)

    finally:
        conn.close()


# -----------------------------
# FETCH DATA
# -----------------------------
def get_all_waste():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, plastic_type, quantity, recyclable
        FROM waste
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


# -----------------------------
# CLEAR DATABASE (OPTIONAL)
# -----------------------------
def clear_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM waste")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='waste'")

    conn.commit()
    conn.close()