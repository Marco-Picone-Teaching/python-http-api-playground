from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from iot_inventory.dto.device_update_request import DeviceUpdateRequest
from iot_inventory.model.device_model import DeviceModel

class DeviceResource(Resource):
    """ Device Resource Class extending the Flask-RESTful Resource """
    def __init__(self, **kwargs):
        self.data_manager = kwargs['data_manager']

    def get(self, location_id, device_id):
        """ GET Method to retrieve a specific device by its location_id and device_id """

        # Check if the provided Location Id in the path is correct
        if location_id in self.data_manager.location_dictionary:

            # Retrieve Location through its location_id
            target_location = self.data_manager.location_dictionary[location_id]

            # Check if the provided Device Id in the path is correct
            if device_id in target_location.device_dictionary:
                # Return the device data and 200 OK code
                return target_location.device_dictionary[device_id].__dict__, 200  # return data and 200 OK code
            else:
                return {'error': "Device Not Found !"}, 404

        else:
            return {'error': "Location Not Found !"}, 404

    def delete(self, location_id, device_id):
        """ DELETE Method to remove a specific device by its location_id and device_id """

        try:

            # Check if the provided Location Id in the path is correct
            if location_id in self.data_manager.location_dictionary:

                # Retrieve Location through its location_id
                target_location = self.data_manager.location_dictionary[location_id]

                if device_id in target_location.device_dictionary:
                    self.data_manager.remove_device(location_id, device_id)
                    return Response(status=204)
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404

        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id, device_id):
        """ PUT Method to update a specific device by its location_id and device_id """

        try:
            # Check if the provided Location Id in the path is correct
            if location_id in self.data_manager.location_dictionary:

                # Retrieve Location through its location_id
                target_location = self.data_manager.location_dictionary[location_id]

                # Check if the provided Device Id in the path is correct
                if device_id in target_location.device_dictionary:
                    # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                    json_data = request.get_json(force=True)

                    # Create a DeviceUpdateRequest object from the JSON data
                    device_update_request = DeviceUpdateRequest(**json_data)

                    # Check if the UUID in the body matches the one in the path
                    if device_update_request.uuid != device_id:
                        return {'error': "UUID mismatch between body and resource"}, 400
                    else:

                        # Create a new DeviceModel object with the updated data
                        update_device_model = DeviceModel(device_id,
                                                          device_update_request.name,
                                                          location_id,
                                                          device_update_request.type,
                                                          device_update_request.manufacturer,
                                                          device_update_request.software_version,
                                                          device_update_request.latitude,
                                                          device_update_request.longitude)

                        # Update the device in the data manager
                        self.data_manager.update_device(location_id, update_device_model)

                        # Return 204 No Content creating a response with no body
                        return Response(status=204)
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
