"""SQLite Database Manager for Wallpaper Metadata."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple
import imagehash

from .config import DB_PATH


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_session(db_path: Path = DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections ensuring clean commit and closure."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: Path = DB_PATH) -> None:
    """Initialize database schema with all required and recommended metadata fields."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallpapers (
                id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                format TEXT NOT NULL,
                filesize INTEGER NOT NULL,
                sha256 TEXT UNIQUE NOT NULL,
                perceptual_hash TEXT,
                source TEXT,
                source_url TEXT,
                ai_confidence REAL,
                duplicate_of INTEGER,
                aspect_ratio TEXT,
                orientation TEXT,
                license TEXT,
                author TEXT,
                title TEXT,
                original_filename TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wallpapers_sha256 ON wallpapers(sha256)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wallpapers_type ON wallpapers(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wallpapers_category ON wallpapers(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wallpapers_phash ON wallpapers(perceptual_hash)")


def get_next_id(db_path: Path = DB_PATH) -> int:
    """Get the next sequential permanent database ID."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM wallpapers")
        row = cursor.fetchone()
        max_id = row[0]
        return 1 if max_id is None else max_id + 1


def insert_wallpaper(metadata: Dict[str, Any], db_path: Path = DB_PATH) -> int:
    """Insert a new wallpaper record into the database."""
    fields = [
        "id", "filename", "type", "category", "width", "height",
        "format", "filesize", "sha256", "perceptual_hash", "source",
        "source_url", "ai_confidence", "duplicate_of", "aspect_ratio",
        "orientation", "license", "author", "title", "original_filename"
    ]

    # Filter metadata to supported fields
    insert_data = {k: metadata.get(k) for k in fields if k in metadata}
    columns = ", ".join(insert_data.keys())
    placeholders = ", ".join("?" for _ in insert_data)
    values = list(insert_data.values())

    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO wallpapers ({columns}) VALUES ({placeholders})",
            values
        )
        return insert_data.get("id", cursor.lastrowid)


def get_wallpaper_by_id(wallpaper_id: int, db_path: Path = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieve wallpaper by permanent ID."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallpapers WHERE id = ?", (wallpaper_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_wallpaper_by_sha256(sha256_hash: str, db_path: Path = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieve wallpaper by SHA-256 hash."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallpapers WHERE sha256 = ?", (sha256_hash,))
        row = cursor.fetchone()
        return dict(row) if row else None


def find_visual_duplicates(
    target_phash: str,
    max_distance: int = 5,
    db_path: Path = DB_PATH
) -> List[Tuple[Dict[str, Any], int]]:
    """
    Search database for visual duplicates using perceptual hash hamming distance.
    Returns list of (wallpaper_dict, distance) tuples sorted by distance.
    """
    if not target_phash:
        return []

    try:
        target_hash = imagehash.hex_to_hash(target_phash)
    except Exception:
        return []

    duplicates = []
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallpapers WHERE perceptual_hash IS NOT NULL")
        for row in cursor.fetchall():
            row_dict = dict(row)
            ph_str = row_dict.get("perceptual_hash")
            if not ph_str:
                continue
            try:
                row_hash = imagehash.hex_to_hash(ph_str)
                distance = target_hash - row_hash
                if distance <= max_distance:
                    duplicates.append((row_dict, distance))
            except Exception:
                continue

    duplicates.sort(key=lambda x: x[1])
    return duplicates


def get_all_wallpapers(db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
    """Get all wallpaper records from the database."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallpapers ORDER BY id ASC")
        return [dict(row) for row in cursor.fetchall()]


def get_stats(db_path: Path = DB_PATH) -> Dict[str, Any]:
    """Calculate overall statistics from the database."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM wallpapers")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT type, COUNT(*) FROM wallpapers GROUP BY type")
        by_type = dict(cursor.fetchall())

        cursor.execute("SELECT category, COUNT(*) FROM wallpapers GROUP BY category ORDER BY COUNT(*) DESC")
        by_category = dict(cursor.fetchall())

        cursor.execute("SELECT orientation, COUNT(*) FROM wallpapers GROUP BY orientation")
        by_orientation = dict(cursor.fetchall())

        cursor.execute("SELECT SUM(filesize) FROM wallpapers")
        total_size = cursor.fetchone()[0] or 0

        cursor.execute("SELECT AVG(width), AVG(height) FROM wallpapers")
        avg_res = cursor.fetchone()

        return {
            "total": total,
            "by_type": by_type,
            "by_category": by_category,
            "by_orientation": by_orientation,
            "total_size_bytes": total_size,
            "avg_width": int(avg_res[0]) if avg_res[0] else 0,
            "avg_height": int(avg_res[1]) if avg_res[1] else 0,
        }
