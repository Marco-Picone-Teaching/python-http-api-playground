import json

class DeviceModel:
    """ IoT Device Class describing the device properties """

    # Device Types
    DEVICE_TYPE_DEFAULT = "device.default"
    DEVICE_TYPE_MOBILE = "device.mobile"
    DEVICE_TYPE_SENSOR = "device.sensor"
    DEVICE_TYPE_ACTUATOR = "device.actuator"

    def __init__(self, uuid, name, location_id, device_type, manufacturer, software_version, latitude, longitude):
        """ Initialize the IoT Device with the provided properties"""
        self.uuid = uuid
        self.name = name
        self.locationId = location_id
        self.type = device_type
        self.manufacturer = manufacturer
        self.software_version = software_version
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        """ Serialize the IoT Device to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
