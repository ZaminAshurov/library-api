import sqlite3


def _conn():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


def find_all():
    with _conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM members").fetchall()]


def find_by_id(member_id):
    with _conn() as conn:
        row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
        return dict(row) if row else None


def find_by_email(email):
    with _conn() as conn:
        row = conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def create(name, email, member_type):
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
            (name, email, member_type),
        )
        return dict(conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone())