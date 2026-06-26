"""
database/db.py
--------------
SQLAlchemy Core helpers for the Chichewa Noun Classifier.

All data access goes through this module — no pandas, numpy, or scipy.

Design:
  - One Engine shared across the application (created at import time).
  - Per-request Connection stored on Flask's `g` object.
  - App must call `app.teardown_appcontext(close_db)` to clean up.
"""

import os
import pathlib
from sqlalchemy import create_engine, text
from flask import g

# ── Engine setup ─────────────────────────────────────────────────────────────
# Build an absolute path to chichewa.db relative to THIS file so the database
# is always found regardless of the working directory (critical for Vercel
# serverless functions where CWD is not the project root).
#
# Override DATABASE_URL env-var to switch to PostgreSQL without code changes.
# e.g.  DATABASE_URL=postgresql://user:pass@host/dbname
_DB_FILE = pathlib.Path(__file__).parent.parent / "chichewa.db"
db_path = _DB_FILE.as_posix()

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///file:{db_path}?mode=ro&uri=true"
)

_engine = create_engine(
    DATABASE_URL,
    # Only required for SQLite; harmless on Postgres.
    connect_args={"check_same_thread": False},
    # Keep a small pool even for SQLite so connections are reused.
    pool_pre_ping=True,
)


# ── Per-request connection ────────────────────────────────────────────────────

def get_db():
    """
    Return a SQLAlchemy Connection for the current Flask request.
    Opens a new connection on first call and stores it on `g`.
    """
    if "db" not in g:
        g.db = _engine.connect()
    return g.db


def close_db(e=None):
    """
    Close the per-request connection.
    Register with: app.teardown_appcontext(close_db)
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ── Query helpers ─────────────────────────────────────────────────────────────

def get_examples(class_key: str, exclude_noun: str = "", n: int = 6) -> list:
    """
    Return up to `n` random singular/plural pairs for `class_key`,
    excluding the noun that was just classified.

    Replaces the pandas-based get_examples() in app.py.
    """
    db = get_db()
    rows = db.execute(
        text("""
            SELECT singular, plural
            FROM   nouns
            WHERE  class_key = :ck
              AND  singular  != :noun
            ORDER  BY RANDOM()
            LIMIT  :n
        """),
        {"ck": class_key, "noun": exclude_noun.lower().strip(), "n": n},
    ).fetchall()
    return [{"singular": r.singular, "plural": r.plural} for r in rows]


def get_class_info(class_key: str) -> dict:
    """
    Return metadata and curated examples for a single noun class.
    Returns an empty dict if the class_key is not found.
    """
    db = get_db()

    row = db.execute(
        text("SELECT * FROM noun_classes WHERE class_key = :ck"),
        {"ck": class_key},
    ).fetchone()

    if not row:
        return {}

    examples = db.execute(
        text("SELECT example FROM class_examples WHERE class_key = :ck"),
        {"ck": class_key},
    ).fetchall()

    return {
        "full_name":       row.full_name,
        "description":     row.description,
        "singular_prefix": row.singular_prefix,
        "plural_prefix":   row.plural_prefix,
        "colour":          row.colour,
        "examples":        [e.example for e in examples],
    }


def get_all_classes() -> list:
    """
    Return all noun classes ordered by their id.
    Used by the /classes route to render the full class listing.
    """
    db = get_db()
    rows = db.execute(
        text("SELECT * FROM noun_classes ORDER BY id")
    ).fetchall()

    result = []
    for row in rows:
        examples = db.execute(
            text("SELECT example FROM class_examples WHERE class_key = :ck"),
            {"ck": row.class_key},
        ).fetchall()
        entry = dict(row._mapping)
        entry["examples"] = [e.example for e in examples]
        result.append(entry)

    return result


def get_engine():
    """Expose the engine for use in migrate.py and tests."""
    return _engine
