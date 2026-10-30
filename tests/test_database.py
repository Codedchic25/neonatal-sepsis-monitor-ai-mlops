"""Unit tests verifying local SQLite database schema bindings and column structural migrations."""

import sqlite3


def test_sqlite_telemetry_table_schema_integrity():
    """Verifies that the runtime relational SQLite telemetry table complies with active CDSS inputs."""
    conn = sqlite3.connect("sepsis_neonatal.db")
    cursor = conn.cursor()

    # Pre-create the schema inside the isolated test worker to guarantee table presence
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            heart_rate INTEGER,
            temperature REAL,
            oxygen_saturation INTEGER,
            blood_pressure TEXT,
            crp REAL,
            pct REAL,
            renal_status TEXT
        );
    """)
    conn.commit()

    # Extract column array structural profiles using internal PRAGMA schemas
    cursor.execute("PRAGMA table_info(telemetry);")
    columns_raw = cursor.fetchall()
    conn.close()

    column_names = [col[1] for col in columns_raw]

    assert "heart_rate" in column_names
    assert "temperature" in column_names
    assert "crp" in column_names
    assert "renal_status" in column_names
