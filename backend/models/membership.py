class Membership:
    def __init__(self, user_id, society_id, role="member"):
        self.user_id = user_id
        self.society_id = society_id
        self.role = role  # Can be "member" or "admin"

    def to_dict(self):
        return self.__dict__
