import json
import os
import sqlite3
from typing import Optional, List

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moments.db")


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS moments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_name TEXT NOT NULL,
                author_avatar_url TEXT,
                content_markdown TEXT NOT NULL,
                content_html TEXT,
                media_json TEXT,
                source TEXT NOT NULL DEFAULT 'model',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )"""
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_moments_created_at ON moments(created_at)")
        c.execute(
            """CREATE TABLE IF NOT EXISTS moment_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                moment_id INTEGER NOT NULL,
                parent_id INTEGER,
                author_name TEXT NOT NULL,
                author_avatar_url TEXT,
                content_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                FOREIGN KEY(moment_id) REFERENCES moments(id),
                FOREIGN KEY(parent_id) REFERENCES moment_comments(id)
            )"""
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_comments_moment_id ON moment_comments(moment_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON moment_comments(parent_id)")


def insert_moment(
    author_name: str,
    content_markdown: str,
    author_avatar_url: Optional[str] = None,
    content_html: Optional[str] = None,
    media: Optional[List[str]] = None,
    source: str = "model",
):
    media_json = json.dumps(media, ensure_ascii=True) if media is not None else None
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            """INSERT INTO moments
               (author_name, author_avatar_url, content_markdown, content_html, media_json, source)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (author_name, author_avatar_url, content_markdown, content_html, media_json, source),
        )
        return c.lastrowid


def list_comments_for_moment_ids(moment_ids):
    if not moment_ids:
        return {}
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        placeholders = ",".join(["?"] * len(moment_ids))
        c.execute(
            f"""SELECT id, moment_id, parent_id, author_name, author_avatar_url,
                      content_text, created_at, updated_at
                 FROM moment_comments
                 WHERE moment_id IN ({placeholders})
                 ORDER BY id ASC""",
            moment_ids,
        )
        rows = c.fetchall()
        grouped = {}
        for row in rows:
            item = {
                "id": row["id"],
                "moment_id": row["moment_id"],
                "parent_id": row["parent_id"],
                "author_name": row["author_name"],
                "author_avatar_url": row["author_avatar_url"],
                "content_text": row["content_text"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            grouped.setdefault(row["moment_id"], []).append(item)
        return grouped


def list_moments(limit: int = 20, offset: int = 0, include_comments: bool = True):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            """SELECT id, author_name, author_avatar_url, content_markdown, content_html,
                      media_json, source, created_at, updated_at
               FROM moments
               ORDER BY id DESC
               LIMIT ? OFFSET ?""",
            (limit, offset),
        )
        rows = c.fetchall()
        comment_map = {}
        if include_comments:
            moment_ids = [row["id"] for row in rows]
            comment_map = list_comments_for_moment_ids(moment_ids)
        results = []
        for row in rows:
            media = json.loads(row["media_json"]) if row["media_json"] else None
            results.append(
                {
                    "id": row["id"],
                    "author_name": row["author_name"],
                    "author_avatar_url": row["author_avatar_url"],
                    "content_markdown": row["content_markdown"],
                    "content_html": row["content_html"],
                    "media": media,
                    "source": row["source"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "comments": comment_map.get(row["id"], []),
                }
            )
        return results


init_db()
