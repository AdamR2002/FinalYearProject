from utils.database import mongo

def get_all_memberships():
    return list(mongo.db.memberships.find({}, {"_id": 0}))

def get_membership_by_id(membership_id):
    return mongo.db.memberships.find_one({"membership_id": membership_id}, {"_id": 0})

def create_membership(membership_data):
    mongo.db.memberships.insert_one(membership_data)
    return membership_data

def delete_membership(membership_id):
    result = mongo.db.memberships.delete_one({"membership_id": membership_id})
    return result.deleted_count > 0
