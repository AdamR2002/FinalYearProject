from utils.database import mongo

def get_all_payments():
    return list(mongo.db.payments.find({}, {"_id": 0}))

def get_payment_by_id(payment_id):
    return mongo.db.payments.find_one({"payment_id": payment_id}, {"_id": 0})

def create_payment(payment_data):
    mongo.db.payments.insert_one(payment_data)
    return payment_data

def update_payment(payment_id, update_data):
    result = mongo.db.payments.update_one({"payment_id": payment_id}, {"$set": update_data})
    return result.modified_count > 0

def delete_payment(payment_id):
    result = mongo.db.payments.delete_one({"payment_id": payment_id})
    return result.deleted_count > 0
