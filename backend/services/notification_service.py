from utils.database import mongo

def get_user_notifications(user_id):
    return list(mongo.db.notifications.find({"user_id": user_id}, {"_id": 0}))

def create_notification(notification_data):
    mongo.db.notifications.insert_one(notification_data)
    return notification_data

def mark_notification_as_read(notification_id):
    result = mongo.db.notifications.update_one({"notification_id": notification_id}, {"$set": {"read": True}})
    return result.modified_count > 0
