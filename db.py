# db.py
import sqlite3

DB_PATH = "instawatch.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                shortcode   TEXT    PRIMARY KEY,
                username    TEXT    NOT NULL,
                date_utc    TEXT    NOT NULL,
                caption     TEXT,
                fetched_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()

def prune_posts(username: str, limit: int):
    """
    Keep only the latest `limit` posts for this username.
    """
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM posts
             WHERE username = ?
               AND shortcode NOT IN (
                   SELECT shortcode
                     FROM posts
                    WHERE username = ?
                    ORDER BY date_utc DESC
                    LIMIT ?
               )
        """, (username, username, limit))
        conn.commit()
