from flask import Blueprint, request, jsonify
from services.payment_service import (
    get_all_payments, get_payment_by_id, create_payment,
    update_payment, delete_payment
)

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


#  Get all payments
@payments_bp.route("/", methods=["GET"])
def get_payments():
    payments = get_all_payments()
    return jsonify({"payments": payments}), 200


#  Get a specific payment by ID
@payments_bp.route("/<payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = get_payment_by_id(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"payment": payment}), 200


#  Create a new payment
@payments_bp.route("/", methods=["POST"])
def add_payment():
    data = request.json
    required_fields = ["user_id", "amount", "currency", "method"]

    #  Ensure required fields exist
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    payment_data = {
        "payment_id": data.get("payment_id"),
        "user_id": data["user_id"],
        "amount": data["amount"],
        "currency": data["currency"],
        "status": data.get("status", "pending"),  # Default: pending
        "method": data["method"],
        "timestamp": data.get("timestamp")
    }

    created_payment = create_payment(payment_data)
    return jsonify({"message": "Payment created successfully", "payment": created_payment}), 201


#  Update a payment
@payments_bp.route("/<payment_id>", methods=["PUT"])
def modify_payment(payment_id):
    data = request.json
    updated = update_payment(payment_id, data)
    if not updated:
        return jsonify({"error": "Payment not found or update failed"}), 404
    return jsonify({"message": f"Payment {payment_id} updated successfully"}), 200


#  Delete a payment
@payments_bp.route("/<payment_id>", methods=["DELETE"])
def remove_payment(payment_id):
    deleted = delete_payment(payment_id)
    if not deleted:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"message": f"Payment {payment_id} deleted successfully"}), 200
