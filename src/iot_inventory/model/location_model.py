import json

class LocationModel:
    """ Location Model describing the location properties """
    def __init__(self, uuid, name, latitude, longitude):
        self.uuid = uuid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.device_dictionary = {}

    @staticmethod
    def from_creation_dto(location_creation_request):
        """ Static Method to create a Location Model from a Location Creation DTO """
        return LocationModel(location_creation_request.uuid,
                             location_creation_request.name,
                             location_creation_request.latitude,
                             location_creation_request.longitude)

    def to_json(self):
        """ Serialize the Location Model to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)