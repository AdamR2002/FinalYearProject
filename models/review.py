class Review:
    def __init__(self, review_id, user_id, society_id, rating, comment, timestamp):
        self.review_id = review_id
        self.user_id = user_id
        self.society_id = society_id
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__
