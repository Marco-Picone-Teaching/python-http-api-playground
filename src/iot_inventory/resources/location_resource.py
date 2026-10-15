from flask import request, Response
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from iot_inventory.dto.location_entity_response import LocationEntityResponse
from iot_inventory.dto.location_update_request import LocationUpdateRequest
from iot_inventory.model.location_model import LocationModel
from iot_inventory.persistence.data_manager import DataManager


class LocationResource(Resource):
    """ Location Resource for handling HTTP requests related to a single Location """


    def __init__(self, **kwargs) -> None:
        """ Constructor injecting the DataManager instance """
        self.data_manager: DataManager = kwargs['data_manager']

    def get(self, location_id: str) -> tuple[dict, int]:
        """ HTTP GET Method to retrieve a single Location Resource """

        # Check if the location exists in the dictionary
        if location_id in self.data_manager.location_dictionary:

            # Retrieve the Location Model from the DataManager
            location = self.data_manager.location_dictionary[location_id]

            # Map the Location Model to the Location Entity Response DTO
            location_entity_response = LocationEntityResponse.from_model(location)

            # Return the serialized data and 200 OK code
            return location_entity_response.__dict__, 200
        else:
            return {'error': "Location Not Found !"}, 404

    def delete(self, location_id: str) -> Response | tuple[dict, int]:
        """ HTTP DELETE Method to remove a single Location Resource """
        try:
            # Check if the location exists in the dictionary
            if location_id in self.data_manager.location_dictionary:
                # Remove the location from the dictionary
                self.data_manager.remove_location(location_id)

                # Return 204 No Content
                return Response(status=204)
            else:
                return {'error': "Location UUID not found"}, 404
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def put(self, location_id: str) -> Response | tuple[dict, int]:
        """ HTTP PUT Method to update a single Location Resource """

        try:
            # Check if the location exists in the dictionary
            if location_id in self.data_manager.location_dictionary:

                # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                location_update_request = LocationUpdateRequest(**json_data)

                # Check if the UUID in the body matches the one in the path
                if location_update_request.uuid != location_id:
                    return {'error': "UUID mismatch between body and resource"}, 400
                else:
                    # Map the Update DTO to a new Location Model with the updated data
                    updated_location_model = LocationModel.from_update_dto(location_update_request)

                    # The update representation does not contain the devices: keep the ones of the current location
                    current_location_model = self.data_manager.location_dictionary[location_id]
                    updated_location_model.device_dictionary = current_location_model.device_dictionary

                    # Update the location in the dictionary
                    self.data_manager.update_location(updated_location_model)

                    # Return 204 No Content
                    return Response(status=204)
            else:
                return {'error': "Location UUID not found"}, 404
        except BadRequest:
            # Raised by get_json() when the body is not a valid JSON
            return {'error': "Invalid JSON ! Check the request"}, 400
        except TypeError as e:
            # Raised by the DTO constructor when the body has missing or unknown fields
            return {'error': "Invalid request body ! Reason: " + str(e)}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
