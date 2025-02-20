from flask import Blueprint, request, jsonify
from services.notification_service import (
    get_user_notifications, create_notification, mark_notification_as_read
)

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

#  Get all notifications for a user
@notifications_bp.route("/<user_id>", methods=["GET"])
def get_notifications(user_id):
    notifications = get_user_notifications(user_id)
    return jsonify({"notifications": notifications})

#  Create a new notification
@notifications_bp.route("/", methods=["POST"])
def add_notification():
    notification_data = request.json
    if not notification_data.get("user_id") or not notification_data.get("message"):
        return jsonify({"error": "Missing required fields: 'user_id' and 'message'"}), 400

    new_notification = create_notification(notification_data)
    return jsonify({"message": "Notification created successfully", "notification": new_notification}), 201

#  Mark a notification as read
@notifications_bp.route("/<notification_id>/read", methods=["PUT"])
def mark_as_read(notification_id):
    updated = mark_notification_as_read(notification_id)
    if not updated:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify({"message": f"Notification {notification_id} marked as read"}), 200
