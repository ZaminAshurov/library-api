from repositories import books_repository
from utils.checks import check_book_deletable, check_exists
from utils.validation import validate_book


def list_books(available_only=False):
    return books_repository.find_all(available_only)


def get_book(book_id):
    book = books_repository.find_by_id(book_id)
    check_exists(book, "book")
    return book


def create_book(data):
    validate_book(data)
    return books_repository.create(data["title"], data["author"], data["isbn"])


def delete_book(book_id):
    book = get_book(book_id)
    check_book_deletable(book)
    books_repository.delete(book_id)