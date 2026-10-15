from iot_inventory.model.device_model import DeviceModel
from iot_inventory.model.location_model import LocationModel

class DataManager:
    """ Data Manager Class to manage the Location and Device Data """

    def __init__(self) -> None:
        """ Initialize the data manager with an empty dictionary to store location data """
        # Instance attribute: each DataManager has its own independent storage
        # The leading underscore marks the attribute as private: it must be accessed only through the methods below
        self._location_dictionary: dict[str, LocationModel] = {}

    def location_exists(self, location_id: str) -> bool:
        """ Check if a location with the given id is stored """
        return location_id in self._location_dictionary

    def get_location(self, location_id: str) -> LocationModel | None:
        """ Retrieve a stored location by its id or None if it does not exist """
        return self._location_dictionary.get(location_id)

    def get_location_list(self) -> list[LocationModel]:
        """ Retrieve the list of the stored locations """
        # Return a new list: adding or removing items from it does not change the internal storage
        return list(self._location_dictionary.values())

    def add_location(self, new_location: LocationModel) -> None:
        """ Store a new location """

        # Check the correct instance for the variable new_location
        if isinstance(new_location, LocationModel):
            self._location_dictionary[new_location.uuid] = new_location
        else:
            raise TypeError("Error adding new Location ! Only LocationModel are allowed !")

    def update_location(self, updated_location: LocationModel) -> None:
        """ Update an existing location """

        # Check the correct instance for the variable updated_location
        if isinstance(updated_location, LocationModel):
            self._location_dictionary[updated_location.uuid] = updated_location
        else:
            raise TypeError("Error updating the Location ! Only LocationModel are allowed !")

    def remove_location(self, location_uuid: str) -> None:
        """ Remove a stored location """
        if location_uuid in self._location_dictionary.keys():
            del self._location_dictionary[location_uuid]

    def device_exists(self, location_id: str, device_id: str) -> bool:
        """ Check if a device with the given id is stored in the given location """
        return location_id in self._location_dictionary and \
            device_id in self._location_dictionary[location_id].device_dictionary

    def get_device(self, location_id: str, device_id: str) -> DeviceModel | None:
        """ Retrieve a stored device by its location id and device id or None if it does not exist """
        target_location = self._location_dictionary.get(location_id)

        if target_location is None:
            return None

        return target_location.device_dictionary.get(device_id)

    def get_device_list(self, location_id: str, device_type: str | None = None) -> list[DeviceModel]:
        """ Retrieve the list of the devices of a location, optionally filtered by device type """

        # Check if the required Location Id is correct
        if location_id in self._location_dictionary:
            target_location = self._location_dictionary[location_id]

            # Build a new list: adding or removing items from it does not change the internal storage
            return [device for device in target_location.device_dictionary.values()
                    if device_type is None or device.type == device_type]
        else:
            raise IndexError("Error Location Id is not correct !")

    def add_device(self, location_id: str, new_device: DeviceModel) -> None:
        """ Store a new device """

        # Check the correct instance for the variable new_device
        if isinstance(new_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self._location_dictionary:
                self._location_dictionary[location_id].device_dictionary[new_device.uuid] = new_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def update_device(self, location_id: str, updated_device: DeviceModel) -> None:
        """ Update an existing device """

        # Check the correct instance for the variable new_device
        if isinstance(updated_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self._location_dictionary:
                self._location_dictionary[location_id].device_dictionary[updated_device.uuid] = updated_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def remove_device(self, location_id: str, device_uuid: str) -> None:
        """ Remove a stored device """

        # Check if the required Location Id is correct
        if location_id in self._location_dictionary:
            # Retrieve the target location object
            target_location = self._location_dictionary[location_id]

            if device_uuid in target_location.device_dictionary.keys():
                del target_location.device_dictionary[device_uuid]
        else:
            raise IndexError("Error Location Id is not correct !")
