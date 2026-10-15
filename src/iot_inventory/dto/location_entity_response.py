import json
from iot_inventory.model.location_model import LocationModel

class LocationEntityResponse:
    """ Location Entity Response DTO Class """
    def __init__(self, uuid: str, name: str, latitude: float, longitude: float, device_list: list[str]) -> None:
        self.uuid = uuid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.device_list = device_list

    @staticmethod
    def from_model(location: LocationModel) -> "LocationEntityResponse":
        """ Static Method to create a Location Entity Response DTO from a Location Model """

        # The internal dictionary of devices is reported as the list of the device ids
        device_id_list = [device.uuid for device in location.device_dictionary.values()]

        return LocationEntityResponse(location.uuid,
                                      location.name,
                                      location.latitude,
                                      location.longitude,
                                      device_id_list)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
