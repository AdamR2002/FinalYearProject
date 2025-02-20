from utils.database import mongo
from utils.helpers import serialize_doc

def get_all_users():
    users = mongo.db.users.find({}, {"_id": 0})
    return [serialize_doc(user) for user in users]

def get_user_by_id(user_id):
    user = mongo.db.users.find_one({"user_id": user_id}, {"_id": 0})
    return serialize_doc(user) if user else None

def create_user(user_data):
    mongo.db.users.insert_one(user_data)
    return user_data

def update_user(user_id, update_data):
    result = mongo.db.users.update_one({"user_id": user_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_user(user_id):
    result = mongo.db.users.delete_one({"user_id": user_id})
    return result.deleted_count > 0
