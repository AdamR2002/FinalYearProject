from utils.database import mongo

def get_all_reviews():
    return list(mongo.db.reviews.find({}, {"_id": 0}))

def get_reviews_by_society(society_id):
    return list(mongo.db.reviews.find({"society_id": society_id}, {"_id": 0}))

def create_review(review_data):
    mongo.db.reviews.insert_one(review_data)
    return review_data

def update_review(review_id, update_data):
    result = mongo.db.reviews.update_one({"review_id": review_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_review(review_id):
    result = mongo.db.reviews.delete_one({"review_id": review_id})
    return result.deleted_count > 0
