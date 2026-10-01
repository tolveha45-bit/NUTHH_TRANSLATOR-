import sqlite3
from datetime import datetime

from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language_mode TEXT DEFAULT 'auto',
            voice_gender TEXT DEFAULT 'female',
            voice_name TEXT DEFAULT '',
            voice_rate TEXT DEFAULT '+0%',
            voice_pitch TEXT DEFAULT '+0Hz',
            voice_volume TEXT DEFAULT '+0%',
            created_at TEXT,
            last_active TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voice_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            source_text TEXT,
            translated_text TEXT,
            source_language TEXT,
            target_language TEXT,
            voice_name TEXT,
            gender TEXT,
            audio_path TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            source_text TEXT,
            translated_text TEXT,
            source_language TEXT,
            target_language TEXT,
            created_at TEXT
        )
    """)

    conn.commit()

    conn.close()


def add_or_update_user(user):

    conn = get_connection()

    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO users (
            user_id,
            username,
            first_name,
            created_at,
            last_active
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_active = excluded.last_active
    """, (
        user.id,
        user.username,
        user.first_name,
        now,
        now
    ))

    conn.commit()

    conn.close()


def get_user(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def update_voice_settings(
    user_id,
    gender=None,
    voice_name=None,
    rate=None,
    pitch=None,
    volume=None
):

    conn = get_connection()

    cursor = conn.cursor()

    current = get_user(user_id)

    if not current:
        conn.close()
        return

    gender = (
        gender
        if gender is not None
        else current["voice_gender"]
    )

    voice_name = (
        voice_name
        if voice_name is not None
        else current["voice_name"]
    )

    rate = (
        rate
        if rate is not None
        else current["voice_rate"]
    )

    pitch = (
        pitch
        if pitch is not None
        else current["voice_pitch"]
    )

    volume = (
        volume
        if volume is not None
        else current["voice_volume"]
    )

    cursor.execute("""
        UPDATE users
        SET
            voice_gender = ?,
            voice_name = ?,
            voice_rate = ?,
            voice_pitch = ?,
            voice_volume = ?,
            last_active = ?
        WHERE user_id = ?
    """, (
        gender,
        voice_name,
        rate,
        pitch,
        volume,
        datetime.now().isoformat(),
        user_id
    ))

    conn.commit()

    conn.close()


def save_voice_history(
    user_id,
    source_text,
    translated_text,
    source_language,
    target_language,
    voice_name,
    gender,
    audio_path
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO voice_history (
            user_id,
            source_text,
            translated_text,
            source_language,
            target_language,
            voice_name,
            gender,
            audio_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        source_text,
        translated_text,
        source_language,
        target_language,
        voice_name,
        gender,
        audio_path,
        datetime.now().isoformat()
    ))

    conn.commit()

    conn.close()


def save_translation(
    user_id,
    source_text,
    translated_text,
    source_language,
    target_language
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO translations (
            user_id,
            source_text,
            translated_text,
            source_language,
            target_language,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        source_text,
        translated_text,
        source_language,
        target_language,
        datetime.now().isoformat()
    ))

    conn.commit()

    conn.close()
