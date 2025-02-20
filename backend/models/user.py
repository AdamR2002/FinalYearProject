class User:
    def __init__(self, user_id, name, email, role, membership=None, events=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.membership = membership or []
        self.events = events or {"attended": [], "registered": []}

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "membership": self.membership,
            "events": self.events
        }
