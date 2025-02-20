from flask import Blueprint, request, jsonify
from services.membership_service import (
    get_all_memberships, get_membership_by_id, create_membership, delete_membership
)

memberships_bp = Blueprint("memberships", __name__, url_prefix="/memberships")

#  Get all memberships
@memberships_bp.route("/", methods=["GET"])
def get_memberships():
    memberships = get_all_memberships()
    return jsonify({"memberships": memberships}), 200

#  Get a specific membership by ID
@memberships_bp.route("/<membership_id>", methods=["GET"])
def get_membership(membership_id):
    membership = get_membership_by_id(membership_id)
    if not membership:
        return jsonify({"error": "Membership not found"}), 404
    return jsonify(membership), 200

#  Create a new membership
@memberships_bp.route("/", methods=["POST"])
def add_membership():
    membership_data = request.json
    if not membership_data.get("user_id") or not membership_data.get("society_id"):
        return jsonify({"error": "Missing required fields: 'user_id' and 'society_id'"}), 400

    new_membership = create_membership(membership_data)
    return jsonify({"message": "Membership created successfully", "membership": new_membership}), 201

#  Delete a membership
@memberships_bp.route("/<membership_id>", methods=["DELETE"])
def remove_membership(membership_id):
    deleted = delete_membership(membership_id)
    if not deleted:
        return jsonify({"error": "Membership not found"}), 404
    return jsonify({"message": f"Membership {membership_id} deleted successfully"}), 200
