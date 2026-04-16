import sqlite3
import os
import logging

# ----------------------------------------------------
# 1. SETUP LOGGING
# ----------------------------------------------------
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 2. RENDER SAFE DATABASE PATH RESOLUTION
# ----------------------------------------------------
# On Render using Persistent disks, data is mapped to /data securely.
# Fallback firmly to local execution space if /data explicitly does not exist natively.
if os.path.exists("/data"):
    DB_PATH = "/data/database.db"
    logger.info("Render Persistent Disk (/data) securely detected.")
else:
    DB_PATH = os.path.join(os.getcwd(), "database.db")
    logger.info("Local Runtime Path securely triggered.")

# ----------------------------------------------------
# 3. CONNECTION POOLING HELPER (SAFE)
# ----------------------------------------------------
def get_db_connection():
    """
    Spawns explicit thread-safe connections mitigating WSGI concurrent locks.
    """
    # Enforce safe OS timeout locks seamlessly locally natively
    conn = sqlite3.connect(DB_PATH, timeout=5.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Force concurrent optimization preventing immediate SQLite 'database locked' crashes seamlessly natively safely
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('PRAGMA journal_mode = WAL')
    conn.execute('PRAGMA busy_timeout = 5000')
    return conn

# ----------------------------------------------------
# 4. INITIALIZATION HOOK
# ----------------------------------------------------
def init_db():
    conn = None
    try:
        conn = get_db_connection()
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
        conn.commit()
        logger.info("Database Schema explicitly verified and securely initialized.")
    except Exception as e:
        logger.error(f"Critical System Database Initialization Error: {e}")
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 5. SAFE INSERT HOOK
# ----------------------------------------------------
def add_waste_log(plastic_type, quantity, recyclable):
    conn = None
    try:
        # Type validation constraint layer natively isolating string injection bounds seamlessly safely natively dynamically
        qty_safe = int(quantity) if quantity is not None else 1
        plastic_safe = str(plastic_type) if plastic_type else "Unknown"
        recyc_safe = str(recyclable) if recyclable else "Unknown"

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO waste (plastic_type, quantity, recyclable) 
            VALUES (?, ?, ?)
        """, (plastic_safe, qty_safe, recyc_safe))
        
        conn.commit()
        logger.info(f"Database Insert Successful: [{plastic_safe}] | Qty: {qty_safe} | Status: {recyc_safe}")
        
    except ValueError as ve:
        logger.warning(f"Integrity Error Processing Entry Quantities: {ve}")
    except sqlite3.Error as sqle:
        if conn:
            conn.rollback() 
        logger.error(f"SQLite Transaction Abort Protocol Triggered: {sqle}")
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"General Execution Pipeline Fault in Database: {e}")
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 6. SAFE READ HOOK
# ----------------------------------------------------
def get_all_waste():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, plastic_type, quantity, recyclable, created_at 
            FROM waste 
            ORDER BY id DESC
        """)
        data = cursor.fetchall()
        return data
        
    except sqlite3.Error as sqle:
        logger.error(f"SQLite Read Extraction Engine Crash: {sqle}")
        return []
    except Exception as e:
        logger.error(f"Database Extraction Route Failure: {e}")
        return []
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 7. DEVELOPMENT HELPER (SAFE)
# ----------------------------------------------------
def clear_database():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM waste")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='waste'")
        conn.commit()
        logger.warning("Database Cleanse Protocol Trigerred (Emptied Sequence Array).")
    except Exception as e:
        logger.error(f"Database Reset Engine Crash: {e}")
    finally:
        if conn:
            conn.close()