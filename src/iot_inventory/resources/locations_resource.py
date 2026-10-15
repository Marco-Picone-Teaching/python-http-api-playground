from flask import request, Response
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from iot_inventory.dto.location_entity_response import LocationEntityResponse
from iot_inventory.dto.location_creation_request import LocationCreationRequest
from iot_inventory.model.location_model import LocationModel
from iot_inventory.persistence.data_manager import DataManager


class LocationsResource(Resource):
    """ Locations Resource Class """

    def __init__(self, **kwargs) -> None:
        """ Initialize the Locations Resource with the provided data manager """
        self.data_manager: DataManager = kwargs['data_manager']

    def post(self) -> Response | tuple[dict, int]:
        """ Create a new Location """
        try:

            # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)

            # Create a Location Creation Request Object
            location_creation_request = LocationCreationRequest(**json_data)

            # Check if the UUID already exists
            if self.data_manager.location_exists(location_creation_request.uuid):
                return {'error': "Location UUID already exists"}, 409
            else:

                # Map the Creation DTO to a new Location Model
                new_location_model = LocationModel.from_creation_dto(location_creation_request)

                # Add the new Location to the Data Manager
                self.data_manager.add_location(new_location_model)

                # Return the Location UUID in the Location Header
                return Response(status=201, headers={"Location": request.url+"/"+new_location_model.uuid})  # Force the No-Content Response
        except BadRequest:
            # Raised by get_json() when the body is not a valid JSON
            return {'error': "Invalid JSON ! Check the request"}, 400
        except TypeError as e:
            # Raised by the DTO constructor when the body has missing or unknown fields
            return {'error': "Invalid request body ! Reason: " + str(e)}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def get(self) -> tuple[list[dict], int]:
        """ Get all Locations """

        # Map each Location Model to a Location Entity Response and build a serializable location list
        result_location_list = [LocationEntityResponse.from_model(location).__dict__
                                for location in self.data_manager.get_location_list()]

        # Return the Location List
        return result_location_list, 200  # return data and 200 OK code
