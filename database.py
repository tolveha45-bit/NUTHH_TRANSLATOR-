import sqlite3

from datetime import datetime

from config import DATABASE_PATH


def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language_mode TEXT DEFAULT 'auto',
            created_at TEXT,
            last_active TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS video_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            source_language TEXT,
            target_language TEXT,
            status TEXT,
            created_at TEXT,
            completed_at TEXT
        )
        """
    )

    connection.commit()

    connection.close()


def add_user(user):

    connection = get_connection()

    now = datetime.utcnow().isoformat()

    connection.execute(
        """
        INSERT INTO users (
            user_id,
            username,
            first_name,
            language_mode,
            created_at,
            last_active
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_active = excluded.last_active
        """,
        (
            user.id,
            user.username,
            user.first_name,
            "auto",
            now,
            now
        )
    )

    connection.commit()

    connection.close()


def create_video_job(
    user_id,
    file_name,
    source_language,
    target_language
):

    connection = get_connection()

    now = datetime.utcnow().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO video_jobs (
            user_id,
            file_name,
            source_language,
            target_language,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            file_name,
            source_language,
            target_language,
            "processing",
            now
        )
    )

    job_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return job_id


def update_video_job(
    job_id,
    status
):

    connection = get_connection()

    completed_at = None

    if status in (
        "completed",
        "failed"
    ):

        completed_at = (
            datetime.utcnow()
            .isoformat()
        )

    connection.execute(
        """
        UPDATE video_jobs
        SET
            status = ?,
            completed_at = ?
        WHERE id = ?
        """,
        (
            status,
            completed_at,
            job_id
        )
    )

    connection.commit()

    connection.close()
