class Event:
    def __init__(self, event_id, name, description, date, time, venue_id, society_id, status="pending", attendees=[]):
        self.event_id = event_id
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.venue_id = venue_id  # Track the venue for the event
        self.society_id = society_id
        self.status = status  # Track if booking is pending, approved, or rejected
        self.attendees = attendees

    def to_dict(self):
        return self.__dict__
