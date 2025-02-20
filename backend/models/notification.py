class Notification:
    def __init__(self, notification_id, user_id, message, timestamp, read=False):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.timestamp = timestamp
        self.read = read

    def to_dict(self):
        return self.__dict__
