from datetime import date, timedelta
from notifications import notifier
from repositories import books_repository, loans_repository, members_repository
from utils.checks import (
    check_book_available,
    check_exists,
    check_fine_payable,
    check_loan_renewable,
    check_loan_returnable,
    check_member_can_borrow,
)
from utils.fine_calculation import calculate_fine, current_loan_fine, days_late, member_total_owed, money
from utils.validation import validate_loan


def list_loans(overdue_only=False):
    loans = loans_repository.find_all()
    if overdue_only:
        loans = [l for l in loans if not l["returned"] and days_late(l["due_date"]) > 0]
    return [{**l, "current_fine": current_loan_fine(l)} for l in loans]


def get_loan(loan_id):
    loan = loans_repository.find_by_id(loan_id)
    check_exists(loan, "loan")
    return {**loan, "current_fine": current_loan_fine(loan)}


def checkout_book(data):
    validate_loan(data)
    book = books_repository.find_by_id(data["book_id"])
    check_exists(book, "book")
    member = members_repository.find_by_id(data["member_id"])
    check_exists(member, "member")
    check_book_available(book)
    check_member_can_borrow(member, loans_repository.find_by_member_id(member["id"]))

    today = date.today()
    due_date = data.get("due_date") or (today + timedelta(days=14)).isoformat()
    loan = loans_repository.create(book["id"], member["id"], due_date, today.isoformat())
    books_repository.set_available(book["id"], False)
    notifier.notify_checkout(member["email"], book["title"])
    return loan


def return_book(loan_id):
    loan = loans_repository.find_by_id(loan_id)
    check_exists(loan, "loan")
    check_loan_returnable(loan)

    fine = calculate_fine(loan["due_date"])
    updated = loans_repository.mark_returned(loan_id, fine)
    books_repository.set_available(loan["book_id"], True)

    member = members_repository.find_by_id(loan["member_id"])
    book = books_repository.find_by_id(loan["book_id"])
    notifier.notify_return(member["email"], book["title"], fine)
    return updated


def renew_loan(loan_id):
    loan = loans_repository.find_by_id(loan_id)
    check_exists(loan, "loan")
    check_loan_renewable(loan)

    new_due = (date.fromisoformat(loan["due_date"]) + timedelta(days=14)).isoformat()
    updated = loans_repository.renew(loan_id, new_due)

    member = members_repository.find_by_id(loan["member_id"])
    book = books_repository.find_by_id(loan["book_id"])
    notifier.notify_renew(member["email"], book["title"])
    return updated


def pay_fine(loan_id):
    loan = loans_repository.find_by_id(loan_id)
    check_exists(loan, "loan")
    check_fine_payable(loan)

    updated = loans_repository.mark_fine_paid(loan_id)
    member = members_repository.find_by_id(loan["member_id"])
    notifier.notify_fine_paid(member["email"], loan["fine"])
    return updated


def overdue_report():
    items = []
    for row in loans_repository.find_open_joined():
        late = days_late(row["due_date"])
        if late > 0:
            items.append({
                "loan_id": row["loan_id"],
                "title": row["title"],
                "member": row["member"],
                "days_late": late,
                "fine": calculate_fine(row["due_date"]),
            })
    return {"items": items, "total_fines": money(sum(i["fine"] for i in items))}


def summary_report():
    loans = loans_repository.find_all()
    return {
        "total_books": books_repository.count_all(),
        "on_loan": sum(1 for l in loans if not l["returned"]),
        "fines_outstanding": member_total_owed(loans),
    }