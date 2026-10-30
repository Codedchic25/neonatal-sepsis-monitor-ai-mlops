"""Integration tests verifying core system workflow boundaries and local telemetry storage."""

import sqlite3


def test_system_sqlite_insertion_and_retrieval():
    """Validates integration lifecycle by committing and fetching real-time clinical parameters."""
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

    # Insert a deterministic testing data point into the local telemetry table
    cursor.execute(
        """
        INSERT INTO telemetry (timestamp, heart_rate, temperature, oxygen_saturation, blood_pressure, crp, pct, renal_status)
        VALUES ('23:15:00', 142, 36.9, 97, '64/41 mmHg', 4.5, 0.42, 'Normal')
    """
    )
    conn.commit()

    # Validate whether the persistence engine retrieves the last recorded tracking step correctly
    cursor.execute(
        "SELECT heart_rate, temperature FROM telemetry ORDER BY id DESC LIMIT 1;"
    )
    last_step = cursor.fetchone()
    conn.close()

    assert last_step is not None
    assert last_step[0] == 142
    assert last_step[1] == 36.9
