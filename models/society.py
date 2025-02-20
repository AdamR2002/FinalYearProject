class Society:
    def __init__(self, society_id, name, description, category, members=[]):
        self.society_id = society_id
        self.name = name
        self.description = description
        self.category = category
        self.members = members  # List of user IDs

    def to_dict(self):
        return self.__dict__
