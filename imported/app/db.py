import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "app.db"


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                nif TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profile_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                file_path TEXT,
                status TEXT NOT NULL,
                score REAL,
                summary TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kpi_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                connection_invites INTEGER DEFAULT 0,
                events_attended INTEGER DEFAULT 0,
                new_connections INTEGER DEFAULT 0,
                profile_views INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS post_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_date TEXT NOT NULL,
                title TEXT NOT NULL,
                format TEXT NOT NULL,
                impressions INTEGER DEFAULT 0,
                reach INTEGER DEFAULT 0,
                saves INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                meaningful_comments INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                dwell_time_seconds INTEGER DEFAULT 0,
                is_case_study INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        _ensure_user_columns(conn)
        _ensure_profile_analysis_columns(conn)
        _ensure_post_entry_columns(conn)


def _ensure_user_columns(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    to_add = {
        "first_name": "TEXT",
        "last_name": "TEXT",
        "phone": "TEXT",
        "nif": "TEXT",
    }
    for column, column_type in to_add.items():
        if column not in columns:
            conn.execute(f"ALTER TABLE users ADD COLUMN {column} {column_type}")


def _ensure_profile_analysis_columns(conn: sqlite3.Connection) -> None:
    columns = {
        row["name"] for row in conn.execute("PRAGMA table_info(profile_analyses)").fetchall()
    }
    to_add = {
        "recommendations": "TEXT",
        "red_flags": "TEXT",
        "report_json": "TEXT",
    }
    for column, column_type in to_add.items():
        if column not in columns:
            conn.execute(f"ALTER TABLE profile_analyses ADD COLUMN {column} {column_type}")


def _ensure_post_entry_columns(conn: sqlite3.Connection) -> None:
    columns = {
        row["name"] for row in conn.execute("PRAGMA table_info(post_entries)").fetchall()
    }
    to_add = {
        "meaningful_comments": "INTEGER DEFAULT 0",
        "shares": "INTEGER DEFAULT 0",
        "dwell_time_seconds": "INTEGER DEFAULT 0",
    }
    for column, column_type in to_add.items():
        if column not in columns:
            conn.execute(f"ALTER TABLE post_entries ADD COLUMN {column} {column_type}")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_user(
    email: str,
    password_hash: str,
    first_name: str,
    last_name: str,
    phone: str,
    nif: str,
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (email, password_hash, first_name, last_name, phone, nif)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (email, password_hash, first_name, last_name, phone, nif),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_user_by_email(email: str):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()


def get_user_by_id(user_id: int):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()


def create_roadmap(user_id: int, title: str, content: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO roadmaps (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content),
        )
        conn.commit()


def list_roadmaps(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM roadmaps WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def create_insight(user_id: int, summary: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO insights (user_id, summary) VALUES (?, ?)",
            (user_id, summary),
        )
        conn.commit()


def list_insights(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM insights WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def create_profile_analysis(
    user_id: int,
    source: str,
    file_path: str | None,
    status: str,
    score: float | None = None,
    summary: str | None = None,
    recommendations: list[str] | None = None,
    red_flags: list[str] | None = None,
    report: list[dict] | None = None,
) -> None:
    with get_conn() as conn:
        recommendations_json = json.dumps(recommendations or [], ensure_ascii=False)
        red_flags_json = json.dumps(red_flags or [], ensure_ascii=False)
        report_json = json.dumps(report or [], ensure_ascii=False)
        conn.execute(
            """
            INSERT INTO profile_analyses (
                user_id,
                source,
                file_path,
                status,
                score,
                summary,
                recommendations,
                red_flags,
                report_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                source,
                file_path,
                status,
                score,
                summary,
                recommendations_json,
                red_flags_json,
                report_json,
            ),
        )
        conn.commit()


def list_profile_analyses(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM profile_analyses WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def create_chat_message(user_id: int, role: str, content: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO chat_messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content),
        )
        conn.commit()


def list_chat_messages(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM chat_messages WHERE user_id = ? ORDER BY created_at ASC",
            (user_id,),
        )
        return cur.fetchall()


def create_kpi_entry(
    user_id: int,
    entry_date: str,
    connection_invites: int,
    events_attended: int,
    new_connections: int,
    profile_views: int,
    notes: str,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO kpi_entries (
                user_id,
                entry_date,
                connection_invites,
                events_attended,
                new_connections,
                profile_views,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                entry_date,
                connection_invites,
                events_attended,
                new_connections,
                profile_views,
                notes,
            ),
        )
        conn.commit()


def list_kpi_entries(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM kpi_entries WHERE user_id = ? ORDER BY entry_date DESC",
            (user_id,),
        )
        return cur.fetchall()


def create_post_entry(
    user_id: int,
    post_date: str,
    title: str,
    format_value: str,
    impressions: int,
    reach: int,
    saves: int,
    comments: int,
    meaningful_comments: int,
    likes: int,
    shares: int,
    clicks: int,
    dwell_time_seconds: int,
    is_case_study: int,
    notes: str,
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO post_entries (
                user_id,
                post_date,
                title,
                format,
                impressions,
                reach,
                saves,
                comments,
                meaningful_comments,
                likes,
                shares,
                clicks,
                dwell_time_seconds,
                is_case_study,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                post_date,
                title,
                format_value,
                impressions,
                reach,
                saves,
                comments,
                meaningful_comments,
                likes,
                shares,
                clicks,
                dwell_time_seconds,
                is_case_study,
                notes,
            ),
        )
        conn.commit()


def list_post_entries(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM post_entries WHERE user_id = ? ORDER BY post_date DESC",
            (user_id,),
        )
        return cur.fetchall()


def get_stats(user_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM roadmaps WHERE user_id = ?) AS roadmaps_count,
                (SELECT COUNT(*) FROM insights WHERE user_id = ?) AS insights_count,
                (SELECT COUNT(*) FROM profile_analyses WHERE user_id = ?) AS analyses_count
            """,
            (user_id, user_id, user_id),
        )
        return cur.fetchone()
