from utils.database import mongo

def get_all_societies():
    return list(mongo.db.societies.find({}, {"_id": 0}))

def get_society_by_id(society_id):
    return mongo.db.societies.find_one({"society_id": society_id}, {"_id": 0})

def create_society(society_data):
    mongo.db.societies.insert_one(society_data)
    return society_data

def update_society(society_id, update_data):
    result = mongo.db.societies.update_one({"society_id": society_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_society(society_id):
    result = mongo.db.societies.delete_one({"society_id": society_id})
    return result.deleted_count > 0
