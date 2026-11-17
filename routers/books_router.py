from flask import Blueprint, jsonify, request
from services import books_service

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["GET"])
def list_books():
    return jsonify(books_service.list_books(request.args.get("available") == "true"))


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return jsonify(books_service.get_book(book_id))


@books_bp.route("/books", methods=["POST"])
def create_book():
    return jsonify(books_service.create_book(request.get_json(silent=True) or {})), 201


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books_service.delete_book(book_id)
    return "", 204