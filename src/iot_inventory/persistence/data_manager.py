from iot_inventory.model.device_model import DeviceModel
from iot_inventory.model.location_model import LocationModel

class DataManager:
    """ Data Manager Class to manage the Location and Device Data """

    def __init__(self) -> None:
        """ Initialize the data manager with an empty dictionary to store location data """
        # Instance attribute: each DataManager has its own independent storage
        self.location_dictionary: dict[str, LocationModel] = {}

    def add_location(self, new_location: LocationModel) -> None:
        """ Store a new location """

        # Check the correct instance for the variable new_location
        if isinstance(new_location, LocationModel):
            self.location_dictionary[new_location.uuid] = new_location
        else:
            raise TypeError("Error adding new Location ! Only LocationModel are allowed !")

    def update_location(self, updated_location: LocationModel) -> None:
        """ Update an existing location """

        # Check the correct instance for the variable updated_location
        if isinstance(updated_location, LocationModel):
            self.location_dictionary[updated_location.uuid] = updated_location
        else:
            raise TypeError("Error updating the Location ! Only LocationModel are allowed !")

    def remove_location(self, location_uuid: str) -> None:
        """ Remove a stored location """
        if location_uuid in self.location_dictionary.keys():
            del self.location_dictionary[location_uuid]

    def add_device(self, location_id: str, new_device: DeviceModel) -> None:
        """ Store a new device """

        # Check the correct instance for the variable new_device
        if isinstance(new_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[new_device.uuid] = new_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def update_device(self, location_id: str, updated_device: DeviceModel) -> None:
        """ Update an existing device """

        # Check the correct instance for the variable new_device
        if isinstance(updated_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[updated_device.uuid] = updated_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def remove_device(self, location_id: str, device_uuid: str) -> None:
        """ Remove a stored device """

        # Check if the required Location Id is correct
        if location_id in self.location_dictionary:
            # Retrieve the target location object
            target_location = self.location_dictionary[location_id]

            if device_uuid in target_location.device_dictionary.keys():
                del target_location.device_dictionary[device_uuid]
        else:
            raise IndexError("Error Location Id is not correct !")
