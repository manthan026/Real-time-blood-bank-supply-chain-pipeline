import os
import sys
import sqlite3
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
# Also check parent directory for .env
parent_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if os.path.exists(parent_env):
    load_dotenv(parent_env)

# Ensure producer can be imported for data generation
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
producer_dir = os.path.join(project_root, "producer")
if producer_dir not in sys.path:
    sys.path.insert(0, producer_dir)

DB_PATH = os.path.join(os.path.dirname(__file__), "blood_bank_local.db")
_db_status = {"is_live": False, "message": "Initializing..."}


def get_secret(key, default=None):
    """Retrieves secret from Streamlit secrets (Cloud) or environment variables."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


def get_db_status():
    """Returns (is_live_mysql, status_message)"""
    return _db_status["is_live"], _db_status["message"]


def get_mysql_connection():
    """Attempts connection to MySQL RDS / Railway MySQL if configured."""
    host = get_secret("MYSQL_HOST") or get_secret("MYSQLHOST")
    port = get_secret("MYSQL_PORT") or get_secret("MYSQLPORT", "3306")
    user = get_secret("MYSQL_USER") or get_secret("MYSQLUSER")
    password = get_secret("MYSQL_PASSWORD") or get_secret("MYSQLPASSWORD")
    database = get_secret("MYSQL_DATABASE") or get_secret("MYSQLDATABASE")

    if not host or host in ("your-rds-endpoint", "your_rds_endpoint", "localhost") and not password:
        return None

    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port) if port else 3306,
            connection_timeout=3
        )
        return conn
    except Exception:
        return None



def _transform_event(event, event_time=None):
    """Transforms a raw event dict into the schema expected by the dashboard and DB."""
    if event_time is None:
        event_time = datetime.now()

    event_type = event.get("event_type", "donation").upper()
    units = int(event.get("units", 0) or 0)
    available_units = int(event.get("available_units", 0) or 0)

    if event_type == "INVENTORY":
        available_units = units if units > 0 else random.randint(30, 200)

    return {
        "event_id": event.get("event_id", str(random.randint(100000, 999999))),
        "event_timestamp": event_time.strftime("%Y-%m-%d %H:%M:%S"),
        "blood_bank": event.get("blood_bank", "Apollo Blood Centre"),
        "city": event.get("city", "Delhi"),
        "state": event.get("state", "Delhi NCR"),
        "event_type": event_type,
        "donor_id": event.get("donor_id", "N/A"),
        "donor_name": event.get("donor_name", "N/A"),
        "age": int(event.get("age", 0) or 0),
        "gender": event.get("gender", "N/A"),
        "blood_group": str(event.get("blood_group", "O+")).upper(),
        "component": event.get("component", "Whole Blood"),
        "units": units,
        "status": str(event.get("status", "SUCCESSFUL")).upper(),
        "request_id": event.get("request_id", "N/A"),
        "hospital": event.get("hospital", event.get("blood_bank", "AIIMS Delhi")),
        "priority": event.get("priority", "N/A"),
        "screening_id": event.get("screening_id", "N/A"),
        "screening_status": event.get("screening_status", "N/A"),
        "transfer_id": event.get("transfer_id", "N/A"),
        "destination_bank": event.get("destination_bank", "N/A"),
        "dispatch_id": event.get("dispatch_id", "N/A"),
        "inventory_id": event.get("inventory_id", "N/A"),
        "available_units": available_units,
        "expiry_id": event.get("expiry_id", "N/A"),
        "expired_units": int(event.get("expired_units", 0) or 0),
        "expiry_date": event.get("expiry_date", "N/A"),
        "alert_id": event.get("alert_id", "N/A"),
        "alert_level": event.get("alert_level", "N/A"),
        "message": event.get("message", "N/A"),
        "processed_time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
        "event_date": event_time.strftime("%Y-%m-%d"),
        "event_hour": event_time.hour
    }


def _seed_local_db():
    """Seeds SQLite with initial realistic streaming events if empty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_donations (
        event_id TEXT PRIMARY KEY,
        event_timestamp TEXT,
        blood_bank TEXT,
        city TEXT,
        state TEXT,
        event_type TEXT,
        donor_id TEXT,
        donor_name TEXT,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        component TEXT,
        units INTEGER,
        status TEXT,
        request_id TEXT,
        hospital TEXT,
        priority TEXT,
        screening_id TEXT,
        screening_status TEXT,
        transfer_id TEXT,
        destination_bank TEXT,
        dispatch_id TEXT,
        inventory_id TEXT,
        available_units INTEGER,
        expiry_id TEXT,
        expired_units INTEGER,
        expiry_date TEXT,
        alert_id TEXT,
        alert_level TEXT,
        message TEXT,
        processed_time TEXT,
        event_date TEXT,
        event_hour INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM blood_donations")
    count = cursor.fetchone()[0]

    try:
        from faker_data import generate_event
    except ImportError:
        from producer.faker_data import generate_event

    now = datetime.now()

    if count < 100:
        records = []
        # Generate 150 events distributed over the last 7 days
        for i in range(150):
            days_ago = random.uniform(0, 6)
            minutes_ago = random.uniform(0, 1440)
            event_time = now - timedelta(days=days_ago, minutes=minutes_ago)
            raw = generate_event()
            rec = _transform_event(raw, event_time)
            records.append(rec)

        cols = list(records[0].keys())
        placeholders = ", ".join(["?"] * len(cols))
        sql = f"INSERT OR REPLACE INTO blood_donations ({', '.join(cols)}) VALUES ({placeholders})"
        cursor.executemany(sql, [[r[c] for c in cols] for r in records])
        conn.commit()

    conn.close()


def _add_live_simulated_event():
    """Adds a new real-time event to the local database to simulate active streaming."""
    try:
        try:
            from faker_data import generate_event
        except ImportError:
            from producer.faker_data import generate_event

        raw = generate_event()
        rec = _transform_event(raw, datetime.now())

        conn = sqlite3.connect(DB_PATH)
        cols = list(rec.keys())
        placeholders = ", ".join(["?"] * len(cols))
        sql = f"INSERT OR REPLACE INTO blood_donations ({', '.join(cols)}) VALUES ({placeholders})"
        conn.cursor().execute(sql, [rec[c] for c in cols])
        conn.commit()
        conn.close()
    except Exception:
        pass


def load_data():
    """
    Loads blood bank data from MySQL RDS if available,
    otherwise loads from the local real-time SQLite database.
    """
    mysql_conn = get_mysql_connection()

    if mysql_conn is not None:
        try:
            query = """
            SELECT *
            FROM blood_donations
            ORDER BY processed_time DESC
            """
            df = pd.read_sql(query, mysql_conn)
            mysql_conn.close()
            _db_status["is_live"] = True
            _db_status["message"] = f"Connected to MySQL RDS ({os.getenv('MYSQL_HOST')})"
            return df
        except Exception as e:
            if mysql_conn:
                mysql_conn.close()

    # Fallback to local SQLite database with live streaming simulation
    _db_status["is_live"] = False
    _db_status["message"] = "Live Simulation Mode (Local Pipeline Engine)"

    _seed_local_db()
    _add_live_simulated_event()

    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT *
    FROM blood_donations
    ORDER BY processed_time DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Ensure correct data types
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0)
    df["available_units"] = pd.to_numeric(df["available_units"], errors="coerce").fillna(0)
    if "event_type" in df.columns:
        df["event_type"] = df["event_type"].str.upper()

    return df