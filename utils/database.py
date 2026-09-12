import sqlite3
import os
from datetime import datetime


# Project root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Database folder
DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

# Create database folder if it doesn't exist
os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

# Database file
DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "phishing_history.db"
)


def get_connection():
    """
    Create and return database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    return connection


def create_table():
    """
    Create detection history table.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detection_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            url TEXT NOT NULL,

            prediction INTEGER NOT NULL,

            confidence REAL,

            detection_type TEXT,

            checked_at TEXT
        )
    """)

    connection.commit()

    connection.close()


def save_detection(
    url,
    prediction,
    confidence,
    detection_type="URL Detection"
):
    """
    Save detection result into database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    checked_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO detection_history
        (
            url,
            prediction,
            confidence,
            detection_type,
            checked_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            url,
            int(prediction),
            float(confidence),
            detection_type,
            checked_at
        )
    )

    connection.commit()

    connection.close()


def get_history():
    """
    Return all detection history,
    newest first.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            url,
            prediction,
            confidence,
            detection_type,
            checked_at

        FROM detection_history

        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def clear_history():
    """
    Delete all detection history.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM detection_history"
    )

    connection.commit()

    connection.close()


# Automatically create table
create_table()