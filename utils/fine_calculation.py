from datetime import date

DAILY_FINE_RATE = 0.50


def money(x):
    return round(float(x), 2)


def days_late(due_date):
    return (date.today() - date.fromisoformat(due_date)).days


def calculate_fine(due_date):
    return money(max(0, days_late(due_date)) * DAILY_FINE_RATE)


def current_loan_fine(loan):
    return calculate_fine(loan["due_date"]) if not loan["returned"] else money(loan["fine"])


def member_total_owed(loans):
    total = 0
    for loan in loans:
        if not loan["returned"]:
            total += calculate_fine(loan["due_date"])
        elif not loan["fine_paid"]:
            total += loan["fine"]
    return money(total)