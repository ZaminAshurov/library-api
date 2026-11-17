import sqlite3


def _conn():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


def _format(row):
    if not row:
        return None
    d = dict(row)
    d["available"] = bool(d["available"])
    return d


def find_all(available_only=False):
    with _conn() as conn:
        sql = "SELECT * FROM books WHERE available = 1" if available_only else "SELECT * FROM books"
        return [_format(r) for r in conn.execute(sql).fetchall()]


def find_by_id(book_id):
    with _conn() as conn:
        return _format(conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone())


def create(title, author, isbn):
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
            (title, author, isbn),
        )
        return _format(conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone())


def set_available(book_id, available):
    with _conn() as conn:
        conn.execute("UPDATE books SET available = ? WHERE id = ?", (int(available), book_id))


def delete(book_id):
    with _conn() as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))


def count_all():
    with _conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]