from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import mongo
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

# ✅ Register User
@auth_bp.route("/register", methods=["POST"])
def register():
    """ Registers a new user ensuring unique email and hashed password """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role", "student")  # Default to "student"
    is_admin = data.get("is_admin", False)  # Default to False unless explicitly set

    if not email or not password or not name:
        return jsonify({"error": "Email, password, and name are required"}), 400

    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    user_id = f"U{mongo.db.users.count_documents({}) + 1}"

    new_user = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "is_admin": is_admin if role == "admin" else False,  # ✅ Admins only if explicitly set
        "membership": data.get("membership", []),
        "events": {"attended": [], "registered": []},
        "password": generate_password_hash(password)
    }

    mongo.db.users.insert_one(new_user)

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# ✅ Login User (Stores Session)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["user_id"]  # ✅ Store user_id in session
        session["is_admin"] = user.get("is_admin", False)  # ✅ Ensure admin status is stored

        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "is_admin": user.get("is_admin", False),  # ✅ Ensure frontend gets admin info
                "membership": user["membership"],
                "events": user["events"]
            }
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ✅ Logout User (Clears Session)
@auth_bp.route("/logout", methods=["POST"])
def logout():
    """ Logs out the user by clearing session """
    session.clear()
    return jsonify({"message": "Successfully logged out"}), 200


# ✅ Get Current Logged-in User
@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    print(f"🔍 Debug: Incoming request -> GET /auth/me")
    print(f"🔍 Debug: Session Data -> {dict(session)}")  # ✅ Print session data

    if "user_id" in session:
        user = mongo.db.users.find_one({"user_id": session["user_id"]}, {"password": 0})
        if user:
            return jsonify(user), 200

    return jsonify({"error": "Not logged in"}), 401


# ✅ Join a Society
@auth_bp.route("/join-society", methods=["POST"])
def join_society():
    """ Allows a logged-in user to join a society """
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    society_id = data.get("society_id")

    if not society_id:
        return jsonify({"error": "Society ID is required"}), 400

    user = mongo.db.users.find_one({"user_id": session["user_id"]})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if society_id in user.get("membership", []):
        return jsonify({"error": "Already a member"}), 400

    mongo.db.users.update_one({"user_id": session["user_id"]}, {"$push": {"membership": society_id}})

    return jsonify({"message": f"Joined society {society_id}"}), 200

@auth_bp.route("/admin-check", methods=["GET"])
def check_admin():
    """ ✅ Checks if the user is an admin """
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = mongo.db.users.find_one({"user_id": session["user_id"]})

    if not user or not user.get("is_admin", False):
        return jsonify({"error": "Access denied"}), 403

    return jsonify({"message": "Admin access granted"}), 200


@auth_bp.route("/promote", methods=["POST"])
def promote_to_admin():
    """ Allows an admin to upgrade a user to admin status """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # ✅ Get the requesting user
    requesting_user = mongo.db.users.find_one({"user_id": session["user_id"]})

    if not requesting_user or not requesting_user.get("is_admin", False):
        return jsonify({"error": "Permission denied"}), 403  # 🚨 Non-admins can't promote

    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = mongo.db.users.find_one({"user_id": user_id})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # ✅ Update the user to admin
    mongo.db.users.update_one({"user_id": user_id}, {"$set": {"is_admin": True, "role": "admin"}})

    return jsonify({"message": f"User {user_id} has been promoted to admin"}), 200

