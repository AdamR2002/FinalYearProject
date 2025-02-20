from flask import Blueprint, request, jsonify
from services.venue_service import (
    get_all_venues,
    get_venue_by_id,
    create_venue,
    update_venue,
    delete_venue
)

venues_bp = Blueprint("venues", __name__)


#  Get all venues
@venues_bp.route("/", methods=["GET"])
def get_venues():
    venues = get_all_venues()
    return jsonify({"venues": venues}), 200


# Get a specific venue by ID
@venues_bp.route("/<venue_id>", methods=["GET"])
def get_venue(venue_id):
    venue = get_venue_by_id(venue_id)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404
    return jsonify(venue), 200


#  Create a new venue
@venues_bp.route("/", methods=["POST"])
def add_venue():
    venue_data = request.json
    if not venue_data.get("venue_id") or not venue_data.get("campus_name"):
        return jsonify({"error": "Missing required fields"}), 400

    created_venue = create_venue(venue_data)
    return jsonify({"message": "Venue created successfully", "venue": created_venue}), 201


#  Update a venue
@venues_bp.route("/<venue_id>", methods=["PUT"])
def modify_venue(venue_id):
    update_data = request.json
    updated = update_venue(venue_id, update_data)
    if not updated:
        return jsonify({"error": "Venue not found or no changes made"}), 404
    return jsonify({"message": "Venue updated successfully"}), 200


#  Delete a venue
@venues_bp.route("/<venue_id>", methods=["DELETE"])
def remove_venue(venue_id):
    deleted = delete_venue(venue_id)
    if not deleted:
        return jsonify({"error": "Venue not found"}), 404
    return jsonify({"message": "Venue deleted successfully"}), 200
