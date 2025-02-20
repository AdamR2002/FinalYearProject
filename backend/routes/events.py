from flask import Blueprint, request, jsonify, session
from services.event_service import (
    create_event, update_event, delete_event, get_event_by_id, get_all_events, register_user_for_event
)
from services.venue_service import get_venue_by_id

events_bp = Blueprint("events", __name__)

# ✅ Get all events
@events_bp.route("/", methods=["GET"])
def fetch_all_events():
    """ Fetch all events from the database """
    events = get_all_events()
    return jsonify({"events": events}), 200

# ✅ Get a single event by ID
@events_bp.route("/<event_id>", methods=["GET"])
def fetch_event(event_id):
    """ Fetch a single event including venue details """
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

# ✅ Create an event (Ensures venue exists)
@events_bp.route("/", methods=["POST"])
def add_event():
    """ Add a new event with venue verification """
    event_data = request.json
    print("Received event data:", event_data)  # ✅ Debugging

    # ✅ Extract venue_id correctly
    venue_id = event_data.get("venue_id")
    if not venue_id:
        return jsonify({"error": "Missing venue_id"}), 400

    # ✅ Validate Required Fields
    required_fields = ["title", "description", "date", "time", "venue_id", "organizing_society"]
    for field in required_fields:
        if field not in event_data or not event_data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # ✅ Ensure venue exists before creating event
    venue = get_venue_by_id(venue_id)
    if not venue:
        return jsonify({"error": f"Venue with ID {venue_id} not found"}), 404

    # ✅ Create event and return response
    new_event = create_event(event_data)
    return jsonify({"message": "Event booking submitted", "event": new_event}), 201

# ✅ Update event status (Approval/Rejection)
@events_bp.route("/<event_id>/status", methods=["PUT"])
def update_event_status(event_id):
    """ Update event approval status """
    status = request.json.get("status")

    # ✅ Ensure status is valid
    if status not in ["approved", "rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    success = update_event(event_id, {"status": status})
    if not success:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({"message": f"Event {event_id} status updated to {status}"}), 200

# ✅ Delete an event (restore venue availability)
@events_bp.route("/<event_id>", methods=["DELETE"])
def remove_event(event_id):
    """ Remove an event and restore venue slot """
    success = delete_event(event_id)
    if not success:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({"message": f"Event {event_id} deleted and venue slot restored"}), 200

# ✅ Event Registration Endpoint
@events_bp.route("/<event_id>/register", methods=["POST"])
def register_for_event(event_id):
    """ Register a user for an event (Ensures user session exists) """

    print("🔍 Debug: Incoming Register Request for Event ID:", event_id)
    print("🔍 Debug: Session Data Before Checking User ID ->", dict(session))  # ✅ Debug session

    if "user_id" not in session:
        print("🚨 Debug: No user_id found in session! User is not logged in.")
        return jsonify({"error": "User must be logged in"}), 401

    user_id = session["user_id"]

    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    success = register_user_for_event(event_id, user_id)

    if not success:
        return jsonify({"error": "User already registered or registration failed"}), 400

    print("✅ Debug: Registration Successful for User:", user_id)
    return jsonify({"message": "Successfully registered for the event"}), 200

