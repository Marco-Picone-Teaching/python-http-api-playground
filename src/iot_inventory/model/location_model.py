import json
from iot_inventory.dto.location_creation_request import LocationCreationRequest
from iot_inventory.dto.location_update_request import LocationUpdateRequest
from iot_inventory.model.device_model import DeviceModel

class LocationModel:
    """ Location Model describing the location properties """
    def __init__(self, uuid: str, name: str, latitude: float, longitude: float) -> None:
        self.uuid = uuid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.device_dictionary: dict[str, DeviceModel] = {}

    @staticmethod
    def from_creation_dto(location_creation_request: LocationCreationRequest) -> "LocationModel":
        """ Static Method to create a Location Model from a Location Creation DTO """
        return LocationModel(location_creation_request.uuid,
                             location_creation_request.name,
                             location_creation_request.latitude,
                             location_creation_request.longitude)

    @staticmethod
    def from_update_dto(location_update_request: LocationUpdateRequest) -> "LocationModel":
        """ Static Method to create a Location Model from a Location Update DTO """
        return LocationModel(location_update_request.uuid,
                             location_update_request.name,
                             location_update_request.latitude,
                             location_update_request.longitude)

    def to_json(self) -> str:
        """ Serialize the Location Model to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
