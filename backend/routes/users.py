from flask import Blueprint, request, jsonify
from services.user_service import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user
)

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify({"users": users})

@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@users_bp.route("/", methods=["POST"])
def create_user_route():
    user_data = request.json
    new_user = create_user(user_data)
    if not new_user:
        return jsonify({"error": "Email already exists"}), 400
    return jsonify({"message": "User created", "user": new_user}), 201

@users_bp.route("/<user_id>", methods=["PUT"])
def update_user_route(user_id):
    update_data = request.json
    updated = update_user(user_id, update_data)
    if not updated:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated successfully"})

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})


