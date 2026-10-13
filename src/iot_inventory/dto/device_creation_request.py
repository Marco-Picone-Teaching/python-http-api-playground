import json

class DeviceCreationRequest:
    """ Device Creation Request DTO """
    def __init__(self, uuid, name, device_type, manufacturer, software_version, latitude, longitude):
        self.uuid = uuid
        self.name = name
        self.type = device_type
        self.manufacturer = manufacturer
        self.software_version = software_version
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        """ Serialize the Device Creation Request to a JSON string """
        return json.dumps(self, default=lambda o: o.__dict__)
