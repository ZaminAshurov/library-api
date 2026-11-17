import sqlite3
from utils.fine_calculation import money


def _conn():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


def _format(row):
    if not row:
        return None
    d = dict(row)
    d["returned"] = bool(d["returned"])
    d["fine"] = money(d["fine"])
    d["fine_paid"] = bool(d["fine_paid"])
    return d


def find_all():
    with _conn() as conn:
        return [_format(r) for r in conn.execute("SELECT * FROM loans").fetchall()]


def find_by_id(loan_id):
    with _conn() as conn:
        return _format(conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone())


def find_by_member_id(member_id):
    with _conn() as conn:
        return [_format(r) for r in conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()]


def find_open_joined():
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT loans.id AS loan_id, books.title, members.name AS member, loans.due_date
            FROM loans
            JOIN books ON books.id = loans.book_id
            JOIN members ON members.id = loans.member_id
            WHERE loans.returned = 0
            """
        ).fetchall()
        return [dict(r) for r in rows]


def create(book_id, member_id, due_date, checked_out):
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
            (book_id, member_id, due_date, checked_out),
        )
        return _format(conn.execute("SELECT * FROM loans WHERE id = ?", (cur.lastrowid,)).fetchone())


def mark_returned(loan_id, fine):
    with _conn() as conn:
        conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
        return _format(conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone())


def renew(loan_id, new_due_date):
    with _conn() as conn:
        conn.execute("UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?", (new_due_date, loan_id))
        return _format(conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone())


def mark_fine_paid(loan_id):
    with _conn() as conn:
        conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
        return _format(conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone())