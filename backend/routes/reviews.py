from flask import Blueprint, request, jsonify
from services.review_service import (
    get_all_reviews, get_reviews_by_society, create_review
)

#  Define Blueprint
reviews_bp = Blueprint("reviews", __name__)

#  Get All Reviews
@reviews_bp.route("/", methods=["GET"])
def get_reviews():
    return jsonify(get_all_reviews())

#  Get Reviews for a Specific Society
@reviews_bp.route("/society/<society_id>", methods=["GET"])
def get_society_reviews(society_id):
    return jsonify(get_reviews_by_society(society_id))

#  Add a Review
@reviews_bp.route("/", methods=["POST"])
def add_review():
    review_data = request.json
    create_review(review_data)
    return jsonify({"message": "Review submitted successfully"}), 201
