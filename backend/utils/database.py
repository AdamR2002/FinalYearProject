from flask_pymongo import PyMongo

mongo = PyMongo()  #  Initialize without an app

def init_db(app):
    """Initialize MongoDB with Flask app"""
    if not app.config.get("MONGO_URI"):
        raise ValueError(f"❌ MONGO_URI is NOT set in app.config! Current config: {app.config}")  #  Show app config

    print(f"🔍 Initializing MongoDB with URI: {app.config['MONGO_URI']}")  #  Log the URI
    mongo.init_app(app)  #  Initialize PyMongo with Flask app


    #  Define collections AFTER initialization
    global users_collection, venues_collection, societies_collection
    global events_collection, memberships_collection, reviews_collection
    global notifications_collection, payments_collection

    users_collection = mongo.db.users
    venues_collection = mongo.db.venues
    societies_collection = mongo.db.societies
    events_collection = mongo.db.events
    memberships_collection = mongo.db.memberships
    reviews_collection = mongo.db.reviews
    notifications_collection = mongo.db.notifications
    payments_collection = mongo.db.payments
