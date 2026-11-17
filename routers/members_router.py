from flask import Blueprint, jsonify, request
from services import members_service

members_bp = Blueprint("members", __name__)


@members_bp.route("/members", methods=["GET"])
def list_members():
    return jsonify(members_service.list_members())


@members_bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    return jsonify(members_service.get_member(member_id))


@members_bp.route("/members", methods=["POST"])
def create_member():
    return jsonify(members_service.create_member(request.get_json(silent=True) or {})), 201


@members_bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    return jsonify(members_service.get_member_loans(member_id))