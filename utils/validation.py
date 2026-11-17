import re
from datetime import date
from errors import http_error


def validate_book(data):
    if not data.get("title") or not data.get("author"):
        raise http_error("title and author are required", 400)
    digits = str(data.get("isbn", "")).replace("-", "")
    if not (digits.isdigit() and len(digits) in (10, 13)):
        raise http_error("invalid isbn", 400)


def validate_member(data):
    if not data.get("name"):
        raise http_error("name is required", 400)
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(data.get("email", ""))):
        raise http_error("invalid email", 400)
    member_type = data.get("type", "student")
    if member_type not in ("student", "staff"):
        raise http_error("type must be student or staff", 400)
    return member_type


def validate_loan(data):
    if not data.get("book_id") or not data.get("member_id"):
        raise http_error("book_id and member_id are required", 400)
    if data.get("due_date"):
        try:
            date.fromisoformat(str(data["due_date"]))
        except ValueError:
            raise http_error("invalid due_date", 400)