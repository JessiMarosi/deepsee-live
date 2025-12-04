import os
import sqlite3
import hashlib
import imagehash
from PIL import Image
from datetime import datetime
from typing import Optional

# Allow environment override for DB path
DB_PATH = os.getenv("DEEPSEE_DB_PATH", "deepsee_trainer.db")

# --- Schema setup ---
def init_db() -> sqlite3.Connection:
    """
    Initialize the SQLite database and ensure required tables exist.
    Returns a connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Images table: stores unique image fingerprints
    cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        sha256 TEXT PRIMARY KEY,
        phash TEXT,
        file_path TEXT,
        first_seen_ts TEXT,
        last_seen_ts TEXT
    )
    """)

    # Events table: chain-of-custody log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sha256 TEXT,
        timestamp TEXT,
        action TEXT,
        actor TEXT,
        details TEXT,
        FOREIGN KEY (sha256) REFERENCES images(sha256)
    )
    """)

    conn.commit()
    return conn

# --- Hash utilities ---
def compute_sha256(path: str) -> str:
    """
    Compute SHA256 hash of a file.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def compute_phash(path: str) -> str:
    """
    Compute perceptual hash (pHash) of an image.
    """
    return str(imagehash.phash(Image.open(path).convert("RGB")))
# --- Logging helpers ---
def log_image(conn: sqlite3.Connection, sha256: str, phash: str, file_path: str):
    """
    Insert or update image metadata in the images table.
    Preserves first_seen_ts if already present.
    """
    ts = datetime.now().isoformat()
    conn.execute("""
    INSERT OR REPLACE INTO images (sha256, phash, file_path, first_seen_ts, last_seen_ts)
    VALUES (?, ?, ?, COALESCE((SELECT first_seen_ts FROM images WHERE sha256=?), ?), ?)
    """, (sha256, phash, file_path, sha256, ts, ts))
    conn.commit()

def log_event(conn: sqlite3.Connection, sha256: Optional[str], action: str,
              actor: str = "trainer_jessi", details: str = ""):
    """
    Log an event into the chain-of-custody table.
    sha256 may be None for system-level events; stored as 'system'.
    """
    ts = datetime.now().isoformat()
    if sha256 is None:
        sha256 = "system"
    conn.execute("""
    INSERT INTO events (sha256, timestamp, action, actor, details)
    VALUES (?, ?, ?, ?, ?)
    """, (sha256, ts, action, actor, details))
    conn.commit()

# --- Duplicate detection ---
def is_near_duplicate(conn: sqlite3.Connection, phash: str, max_dist: int = 5) -> bool:
    """
    Check if the given perceptual hash is near-duplicate of any stored image.
    Guards against NULL or malformed phash entries.
    """
    rows = conn.execute("SELECT phash FROM images").fetchall()
    for r in rows:
        stored_phash = r[0]
        if not stored_phash:
            continue
        try:
            if imagehash.hex_to_hash(stored_phash) - imagehash.hex_to_hash(phash) <= max_dist:
                return True
        except Exception:
            continue
    return False
# --- Retrain trigger logic ---
def should_retrain(conn: sqlite3.Connection,
                   min_new_flags: int = 50,
                   min_ratio: float = 0.4,
                   max_ratio: float = 0.6) -> bool:
    """
    Decide if retraining should be triggered based on number of new flags
    and class balance ratio (AI vs Human).
    Returns True if retraining criteria are met, otherwise False.
    """
    flags = conn.execute("SELECT details FROM events WHERE action='trainer_flag'").fetchall()
    total = len(flags)
    if total < min_new_flags:
        return False

    ai_flags = sum(1 for f in flags if "AI" in f[0])
    human_flags = sum(1 for f in flags if "Human" in f[0])

    if total == 0:
        return False

    ratio = ai_flags / total
    return min_ratio <= ratio <= max_ratio
