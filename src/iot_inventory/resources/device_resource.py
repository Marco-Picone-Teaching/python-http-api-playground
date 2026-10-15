from flask import request, Response
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from iot_inventory.dto.device_entity_response import DeviceEntityResponse
from iot_inventory.dto.device_update_request import DeviceUpdateRequest
from iot_inventory.model.device_model import DeviceModel
from iot_inventory.persistence.data_manager import DataManager

class DeviceResource(Resource):
    """ Device Resource Class extending the Flask-RESTful Resource """
    def __init__(self, **kwargs) -> None:
        self.data_manager: DataManager = kwargs['data_manager']

    def get(self, location_id: str, device_id: str) -> tuple[dict, int]:
        """ GET Method to retrieve a specific device by its location_id and device_id """

        # Check if the provided Location Id in the path is correct
        if self.data_manager.location_exists(location_id):

            # Retrieve the Device Model from the DataManager (None if it does not exist)
            device = self.data_manager.get_device(location_id, device_id)

            if device is not None:
                # Map the Device Model to the Device Entity Response DTO
                device_entity_response = DeviceEntityResponse.from_model(device)

                # Return the device data and 200 OK code
                return device_entity_response.__dict__, 200
            else:
                return {'error': "Device Not Found !"}, 404

        else:
            return {'error': "Location Not Found !"}, 404

    def delete(self, location_id: str, device_id: str) -> Response | tuple[dict, int]:
        """ DELETE Method to remove a specific device by its location_id and device_id """

        try:

            # Check if the provided Location Id in the path is correct
            if self.data_manager.location_exists(location_id):

                # Check if the provided Device Id in the path is correct
                if self.data_manager.device_exists(location_id, device_id):
                    self.data_manager.remove_device(location_id, device_id)
                    return Response(status=204)
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404

        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id: str, device_id: str) -> Response | tuple[dict, int]:
        """ PUT Method to update a specific device by its location_id and device_id """

        try:
            # Check if the provided Location Id in the path is correct
            if self.data_manager.location_exists(location_id):

                # Check if the provided Device Id in the path is correct
                if self.data_manager.device_exists(location_id, device_id):
                    # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                    json_data = request.get_json(force=True)

                    # Create a DeviceUpdateRequest object from the JSON data
                    device_update_request = DeviceUpdateRequest(**json_data)

                    # Check if the UUID in the body matches the one in the path
                    if device_update_request.uuid != device_id:
                        return {'error': "UUID mismatch between body and resource"}, 400
                    else:

                        # Map the Update DTO and the location_id of the URI to a new Device Model
                        update_device_model = DeviceModel.from_update_dto(location_id, device_update_request)

                        # Update the device in the data manager
                        self.data_manager.update_device(location_id, update_device_model)

                        # Return 204 No Content creating a response with no body
                        return Response(status=204)
                else:
                    return {'error': "Device UUID not found"}, 404
            else:
                return {'error': "Location Not Found !"}, 404
        except BadRequest:
            # Raised by get_json() when the body is not a valid JSON
            return {'error': "Invalid JSON ! Check the request"}, 400
        except TypeError as e:
            # Raised by the DTO constructor when the body has missing or unknown fields
            return {'error': "Invalid request body ! Reason: " + str(e)}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
