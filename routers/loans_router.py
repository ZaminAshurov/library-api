from flask import Blueprint, jsonify, request
from services import loans_service

loans_bp = Blueprint("loans", __name__)


@loans_bp.route("/loans", methods=["GET"])
def list_loans():
    return jsonify(loans_service.list_loans(request.args.get("overdue") == "true"))


@loans_bp.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    return jsonify(loans_service.get_loan(loan_id))


@loans_bp.route("/loans", methods=["POST"])
def create_loan():
    return jsonify(loans_service.checkout_book(request.get_json(silent=True) or {})), 201


@loans_bp.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    return jsonify(loans_service.return_book(loan_id))


@loans_bp.route("/loans/<int:loan_id>/renew", methods=["POST"])
def renew_loan(loan_id):
    return jsonify(loans_service.renew_loan(loan_id))


@loans_bp.route("/loans/<int:loan_id>/pay-fine", methods=["POST"])
def pay_fine(loan_id):
    return jsonify(loans_service.pay_fine(loan_id))


@loans_bp.route("/reports/overdue", methods=["GET"])
def report_overdue():
    return jsonify(loans_service.overdue_report())


@loans_bp.route("/reports/summary", methods=["GET"])
def report_summary():
    return jsonify(loans_service.summary_report())