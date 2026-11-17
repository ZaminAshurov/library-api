from repositories import loans_repository, members_repository
from utils.checks import check_email_available, check_exists, loan_limit_for
from utils.fine_calculation import member_total_owed
from utils.validation import validate_member


def list_members():
    return members_repository.find_all()


def get_member(member_id):
    member = members_repository.find_by_id(member_id)
    check_exists(member, "member")
    return member


def create_member(data):
    member_type = validate_member(data)
    check_email_available(members_repository.find_by_email(data["email"]))
    return members_repository.create(data["name"], data["email"], member_type)


def get_member_loans(member_id):
    member = get_member(member_id)
    loans = loans_repository.find_by_member_id(member_id)
    open_count = sum(1 for l in loans if not l["returned"])
    summary = [
        {k: l[k] for k in ("id", "book_id", "due_date", "returned", "fine", "fine_paid")}
        for l in loans
    ]
    return {
        "loans": summary,
        "total_owed": member_total_owed(loans),
        "loans_remaining": loan_limit_for(member) - open_count,
    }