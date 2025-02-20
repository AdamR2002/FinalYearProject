class Venue:
    def __init__(self, venue_id, campus_name, building_name, room_name, capacity, features, booking_requirements, available_slots=[]):
        self.venue_id = venue_id
        self.campus_name = campus_name  # Campus where the venue is located
        self.building_name = building_name  # Building where the venue is located
        self.room_name = room_name  # Specific room name
        self.capacity = capacity  # Maximum capacity of the room
        self.features = features  # List of available amenities
        self.booking_requirements = booking_requirements  # Special requirements for booking
        self.available_slots = available_slots  # List of available booking slots

    def to_dict(self):
        """Convert class object to a dictionary for MongoDB storage."""
        return self.__dict__
