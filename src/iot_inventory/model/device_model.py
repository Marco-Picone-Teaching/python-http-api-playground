import json
from iot_inventory.dto.device_creation_request import DeviceCreationRequest
from iot_inventory.dto.device_update_request import DeviceUpdateRequest

class DeviceModel:
    """ IoT Device Class describing the device properties """

    # Device Types
    DEVICE_TYPE_DEFAULT = "device.default"
    DEVICE_TYPE_MOBILE = "device.mobile"
    DEVICE_TYPE_SENSOR = "device.sensor"
    DEVICE_TYPE_ACTUATOR = "device.actuator"

    def __init__(self, uuid: str, name: str, location_id: str, device_type: str, manufacturer: str,
                 software_version: str, latitude: float, longitude: float) -> None:
        """ Initialize the IoT Device with the provided properties"""
        self.uuid = uuid
        self.name = name
        self.locationId = location_id
        self.type = device_type
        self.manufacturer = manufacturer
        self.software_version = software_version
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_creation_dto(location_id: str, device_creation_request: DeviceCreationRequest) -> "DeviceModel":
        """ Static Method to create a Device Model from a Device Creation DTO and the Location Id of the URI """
        return DeviceModel(device_creation_request.uuid,
                           device_creation_request.name,
                           location_id,
                           device_creation_request.type,
                           device_creation_request.manufacturer,
                           device_creation_request.software_version,
                           device_creation_request.latitude,
                           device_creation_request.longitude)

    @staticmethod
    def from_update_dto(location_id: str, device_update_request: DeviceUpdateRequest) -> "DeviceModel":
        """ Static Method to create a Device Model from a Device Update DTO and the Location Id of the URI """
        return DeviceModel(device_update_request.uuid,
                           device_update_request.name,
                           location_id,
                           device_update_request.type,
                           device_update_request.manufacturer,
                           device_update_request.software_version,
                           device_update_request.latitude,
                           device_update_request.longitude)

    def to_json(self) -> str:
        """ Serialize the IoT Device to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
