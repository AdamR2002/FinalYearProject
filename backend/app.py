from flask import Flask, jsonify, request, session
from flask_cors import CORS
from utils.database import init_db
from routes.users import users_bp
from routes.venues import venues_bp
from routes.societies import societies_bp
from routes.reviews import reviews_bp
from routes.notifications import notifications_bp
from routes.memberships import memberships_bp
from routes.events import events_bp
from routes.payments import payments_bp
from routes.auth import auth_bp
from flask_session import Session

app = Flask(__name__)

# ✅ Improved CORS Configuration
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# ✅ Set MongoDB URI BEFORE initializing the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/Society"

# ✅ REQUIRED: Set Secret Key for Flask Sessions
app.config["SECRET_KEY"] = "somethingunique"

# ✅ Flask Session Configuration (Ensure Cookie Persists)
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions on disk
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True  # Protect session cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access
app.config["SESSION_COOKIE_SECURE"] = True  # 🔧 Must be True for "None", False if testing on HTTP
app.config["SESSION_COOKIE_SAMESITE"] = "None"  # 🔧 "None" required for cross-origin cookies
Session(app)  # ✅ Initialize Flask-Session

# ✅ Initialize Database
init_db(app)

# ✅ Register Blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(venues_bp, url_prefix="/venues")
app.register_blueprint(societies_bp, url_prefix="/societies")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(notifications_bp, url_prefix="/notifications")
app.register_blueprint(memberships_bp, url_prefix="/memberships")
app.register_blueprint(events_bp, url_prefix="/events")
app.register_blueprint(payments_bp, url_prefix="/payments")
app.register_blueprint(auth_bp, url_prefix="/auth")

# ✅ Debugging: Print Session Data Before Every Request
@app.before_request
def debug_session():
    print(f"🔍 Debug: Incoming request -> {request.method} {request.path}")
    print(f"🔍 Debug: Session Data -> {dict(session)}")

# ✅ Debug Route: Manually Check Session in Browser
@app.route("/session-debug", methods=["GET"])
def session_debug():
    return jsonify({"session_data": dict(session)})

# ✅ Handle Preflight Requests (CORS)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Set-Cookie")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

if __name__ == "__main__":
    app.run(debug=True)
