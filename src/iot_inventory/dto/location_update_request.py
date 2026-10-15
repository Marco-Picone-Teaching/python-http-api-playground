import json

class LocationUpdateRequest:
    """ Location Update Request DTO Class """
    def __init__(self, uuid: str, name: str, latitude: float, longitude: float) -> None:
        self.uuid = uuid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self) -> str:
        """ Serialize the Location Update Request to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
