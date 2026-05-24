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
# On Vercel, the filesystem is read-only except for /tmp.
# Fallback firmly to local execution space if no specific cloud environment is detected.
if os.path.exists("/data"):
    DB_PATH = "/data/database.db"
    logger.info("Render Persistent Disk (/data) securely detected.")
elif os.environ.get("VERCEL"):
    DB_PATH = "/tmp/database.db"
    logger.info("Vercel Serverless environment detected. Using /tmp for transient storage.")
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
        
        # Core Waste Table with GPS and User ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS waste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plastic_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                recyclable TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                user_id TEXT,
                points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Simulated IoT Bin Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iot_bins (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                fill_level INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Seed bins if empty
        cursor.execute("SELECT COUNT(*) FROM iot_bins")
        if cursor.fetchone()[0] == 0:
            bins = [
                (1, 'Central Market', 45),
                (2, 'City Park', 85),
                (3, 'Tech Hub Entrance', 12)
            ]
            cursor.executemany("INSERT INTO iot_bins (id, location, fill_level) VALUES (?, ?, ?)", bins)
            
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
def add_waste_log(plastic_type, quantity, recyclable, lat=None, lon=None, user_id="Anonymous"):
    conn = None
    try:
        qty_safe = int(quantity) if quantity is not None else 1
        plastic_safe = str(plastic_type) if plastic_type else "Unknown"
        recyc_safe = str(recyclable) if recyclable else "Unknown"
        
        # Logic for Rewards System: Award points for recyclable plastic
        points = 0
        if "yes" in recyc_safe.lower():
            points = qty_safe * 10 

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO waste (plastic_type, quantity, recyclable, latitude, longitude, user_id, points) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (plastic_safe, qty_safe, recyc_safe, lat, lon, user_id, points))
        
        conn.commit()
        logger.info(f"Database Insert Successful: [{plastic_safe}] | Qty: {qty_safe} | Status: {recyc_safe} | Points: {points}")
        
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
            SELECT id, plastic_type, quantity, recyclable, latitude, longitude, user_id, points, created_at 
            FROM waste 
            ORDER BY id DESC
        """)
        data = cursor.fetchall()
        return data
    except Exception as e:
        logger.error(f"Database Extraction Route Failure: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_iot_status():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, location, fill_level, last_updated FROM iot_bins")
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"IoT Data Extraction Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_leaderboard():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, SUM(points) as total_points 
            FROM waste 
            GROUP BY user_id 
            ORDER BY total_points DESC 
            LIMIT 5
        """)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Leaderboard Extraction Error: {e}")
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