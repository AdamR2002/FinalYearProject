from utils.database import mongo

def get_all_venues():
    """Retrieve all venues from MongoDB."""
    return list(mongo.db.venues.find({}, {"_id": 0}))

def get_venue_by_id(venue_id):
    """Retrieve a venue by its ID."""
    return mongo.db.venues.find_one({"venue_id": venue_id}, {"_id": 0})

def create_venue(venue_data):
    """Insert a new venue into the database."""
    mongo.db.venues.insert_one(venue_data)
    return venue_data

def update_venue(venue_id, update_data):
    """Update a venue by its ID."""
    result = mongo.db.venues.update_one({"venue_id": venue_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_venue(venue_id):
    """Delete a venue by its ID."""
    result = mongo.db.venues.delete_one({"venue_id": venue_id})
    return result.deleted_count > 0
