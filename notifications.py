from utils.fine_calculation import money


class MockNotifier:
    """Mock object for email notifications."""

    def __init__(self, outbox_path="outbox.txt"):
        self.outbox_path = outbox_path
        self.sent = []

    def send(self, to_email, subject, body, enabled=True):
        if not enabled:
            return
        entry = f"TO: {to_email} | SUBJECT: {subject} | BODY: {body}"
        self.sent.append(entry)
        with open(self.outbox_path, "a") as f:
            f.write(entry + "\n")

    def notify_checkout(self, email, title):
        self.send(email, "Book checked out", f"You checked out {title}")

    def notify_renew(self, email, title):
        self.send(email, "Loan renewed", f"You renewed {title}")

    def notify_return(self, email, title, fine):
        self.send(email, "Book returned", f"You returned {title}. Fine: ${money(fine)}")

    def notify_fine_paid(self, email, amount):
        self.send(email, "Fine paid", f"We received ${money(amount)}")


notifier = MockNotifier()