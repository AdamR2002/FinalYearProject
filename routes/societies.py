from flask import Blueprint, request, jsonify, session
from services.society_service import (
    get_all_societies,
    get_society_by_id,
    create_society,
    update_society,
    delete_society
)
from utils import mongo

societies_bp = Blueprint("societies", __name__)

# ✅ Get All Societies (Only Active)
@societies_bp.route("/", methods=["GET"])
def get_societies():
    societies = mongo.db.societies.find({"status": "active"}, {"_id": 0})  # Fetch active societies only
    return jsonify({"societies": list(societies)})


# ✅ Get Specific Society by ID (Including Members & Events)
@societies_bp.route("/<society_id>", methods=["GET"])
def get_society(society_id):
    society = mongo.db.societies.find_one({"society_id": society_id, "status": "active"}, {"_id": 0})

    if not society:
        return jsonify({"error": "Society not found"}), 404

    # Fetch Members & Managed Events
    society["members"] = [
        user["name"] for user in mongo.db.users.find({"membership": society_id}, {"_id": 0, "name": 1})
    ]
    society["events_managed"] = [
        event["event_id"] for event in mongo.db.events.find({"society_id": society_id}, {"_id": 0, "event_id": 1})
    ]

    return jsonify(society)


# ✅ Create a New Society (Admins Only)
@societies_bp.route("/", methods=["POST"])
def add_society():
    if "user_id" not in session or not session.get("is_admin", False):
        return jsonify({"error": "Unauthorized access"}), 403  # 🚨 Admins only

    society_data = request.json
    if not society_data or "name" not in society_data or "campus" not in society_data:
        return jsonify({"error": "Name and campus are required"}), 400

    society_id = f"S{mongo.db.societies.count_documents({}) + 1}"

    new_society = {
        "society_id": society_id,
        "name": society_data["name"],
        "campus": society_data["campus"],
        "moderators": [],  # Empty by default
        "status": "active"
    }

    mongo.db.societies.insert_one(new_society)
    return jsonify({"message": "Society created successfully", "society": new_society}), 201


# ✅ Update Society (Admins Only)
@societies_bp.route("/<society_id>", methods=["PUT"])
def modify_society(society_id):
    if "user_id" not in session or not session.get("is_admin", False):
        return jsonify({"error": "Unauthorized access"}), 403  # 🚨 Admins only

    update_data = request.json
    updated = update_society(society_id, update_data)

    if not updated:
        return jsonify({"error": "Society not found or no changes made"}), 404

    return jsonify({"message": "Society updated successfully"})


# ✅ Soft Delete Society (Admins Only)
@societies_bp.route("/<society_id>", methods=["DELETE"])
def remove_society(society_id):
    if "user_id" not in session or not session.get("is_admin", False):
        return jsonify({"error": "Unauthorized access"}), 403  # 🚨 Admins only

    society = mongo.db.societies.find_one({"society_id": society_id})

    if not society:
        return jsonify({"error": "Society not found"}), 404

    # Soft delete: Update status instead of removing
    mongo.db.societies.update_one({"society_id": society_id}, {"$set": {"status": "inactive"}})

    return jsonify({"message": "Society has been deactivated"}), 200
