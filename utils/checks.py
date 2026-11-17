from datetime import date
from errors import http_error
from utils.fine_calculation import member_total_owed


def loan_limit_for(member):
    return 5 if member["type"] == "staff" else 3


def check_exists(item, label):
    if item is None:
        raise http_error(f"{label} not found", 404)


def check_book_deletable(book):
    if not book["available"]:
        raise http_error("book is on loan", 409)


def check_book_available(book):
    if not book["available"]:
        raise http_error("book is not available", 409)


def check_email_available(existing_member):
    if existing_member is not None:
        raise http_error("email already registered", 409)


def check_member_can_borrow(member, member_loans):
    if member_total_owed(member_loans) > 0:
        raise http_error("member has unpaid fines", 409)
    open_loans = sum(1 for l in member_loans if not l["returned"])
    if open_loans >= loan_limit_for(member):
        raise http_error("loan limit reached", 409)


def check_loan_returnable(loan):
    if loan["returned"]:
        raise http_error("loan already returned", 409)


def check_loan_renewable(loan):
    check_loan_returnable(loan)
    if date.fromisoformat(loan["due_date"]) < date.today():
        raise http_error("overdue loans cannot be renewed", 409)
    if loan["renewals"] >= 1:
        raise http_error("loan was already renewed", 409)


def check_fine_payable(loan):
    if not loan["returned"]:
        raise http_error("return the book before paying", 409)
    if loan["fine"] <= 0 or loan["fine_paid"]:
        raise http_error("no fine to pay", 409)