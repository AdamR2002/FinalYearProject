
from bson import ObjectId
from services.venue_service import get_venue_by_id
from utils.database import mongo

def get_all_events():
    return list(mongo.db.events.find({}, {"_id": 0}))


def get_event_by_id(event_id):
    """ Retrieve an event by `event_id` (E###) or `_id` (MongoDB ObjectId) """

    # Check if event_id is in `E###` format
    if event_id.startswith("E"):
        query = {"event_id": event_id}
    else:
        try:
            query = {"_id": ObjectId(event_id)}
        except Exception:
            return None  # Invalid ObjectId format

    event = mongo.db.events.find_one(query)
    return event if event else None


def create_event(event_data):

    last_event = mongo.db.events.find_one(sort=[("event_id", -1)])
    next_event_id = f"E00{int(last_event['event_id'][3:]) + 1}" if last_event else "E001"


    event = {
        "_id": ObjectId(),  # ✅ Ensures MongoDB assigns a unique ObjectId
        "event_id": event_data.get("event_id", next_event_id),  # ✅ Ensures uniqueness
        "title": event_data["title"],
        "description": event_data["description"],
        "date": event_data["date"],
        "time": event_data["time"],
        "organizing_society": event_data["organizing_society"],
        "venue": event_data["venue"],
        "ticketing": event_data.get("ticketing", {
            "type": "free",
            "max_attendees": 50,
            "registered_users": []
        }),
        "status": event_data.get("status", "upcoming"),
        "attendees": event_data.get("attendees", [])
    }

    # Insert into MongoDB
    mongo.db.events.insert_one(event)
    return event

def update_event(event_id, update_data):
    """ Update an event, e.g., change status """
    result = mongo.db.events.update_one({"event_id": event_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_event(event_id):
    """ Delete an event and restore its booked time slot """
    event = mongo.db.events.find_one({"event_id": event_id})
    if not event:
        return False

    #  Restore the booked slot in the venue
    mongo.db.venues.update_one(
        {"venue_id": event["venue_id"]},
        {"$push": {"available_slots": {"date": event["date"], "time": event["time"]}}}
    )

    # Delete the event
    result = mongo.db.events.delete_one({"event_id": event_id})
    return result.deleted_count > 0


def register_user_for_event(event_id, user_id):
    """ Registers a user for an event and updates both the event & user in MongoDB """

    event = mongo.db.events.find_one({"event_id": event_id})
    user = mongo.db.users.find_one({"user_id": user_id})

    if not event or not user:
        return False  # 🚨 Either the event or user does not exist

    # ✅ Ensure `attendees` array exists in the event
    if "attendees" not in event:
        event["attendees"] = []

    if user_id in event["attendees"]:
        return False  # 🚨 User is already registered

    # ✅ Add user to event's attendee list
    mongo.db.events.update_one(
        {"event_id": event_id},
        {"$push": {"attendees": user_id}}
    )

    # ✅ Ensure `registered` array exists in user's document
    if "events" not in user:
        user["events"] = {"attended": [], "registered": []}

    if "registered" not in user["events"]:
        user["events"]["registered"] = []

    # ✅ Add event to user's registered events
    mongo.db.users.update_one(
        {"user_id": user_id},
        {"$push": {"events.registered": event_id}}
    )

    return True  # ✅ Registration successful
