import json
from iot_inventory.model.device_model import DeviceModel

class DeviceEntityResponse:
    """ Device Entity Response DTO Class """
    def __init__(self, uuid: str, name: str, location_id: str, device_type: str, manufacturer: str,
                 software_version: str, latitude: float, longitude: float) -> None:
        self.uuid = uuid
        self.name = name
        self.locationId = location_id
        self.type = device_type
        self.manufacturer = manufacturer
        self.software_version = software_version
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_model(device: DeviceModel) -> "DeviceEntityResponse":
        """ Static Method to create a Device Entity Response DTO from a Device Model """
        return DeviceEntityResponse(device.uuid,
                                    device.name,
                                    device.locationId,
                                    device.type,
                                    device.manufacturer,
                                    device.software_version,
                                    device.latitude,
                                    device.longitude)

    def to_json(self) -> str:
        """ Serialize the Device Entity Response to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
