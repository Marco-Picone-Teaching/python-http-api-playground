from flask import request, Response
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from iot_inventory.dto.device_creation_request import DeviceCreationRequest
from iot_inventory.dto.device_entity_response import DeviceEntityResponse
from iot_inventory.model.device_model import DeviceModel
from iot_inventory.persistence.data_manager import DataManager

class DevicesResource(Resource):
    """ Devices Resource Class """

    def __init__(self, **kwargs) -> None:
        """ Initialize the Devices Resource with the DataManager """
        self.data_manager: DataManager = kwargs['data_manager']

    def post(self, location_id: str) -> Response | tuple[dict, int]:
        """ Create a new Device in the specified Location """

        try:
            # Check if the location is correct
            if self.data_manager.location_exists(location_id):

                # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                device_creation_request = DeviceCreationRequest(**json_data)

                # Check if the device is new or if it already exists
                if self.data_manager.device_exists(location_id, device_creation_request.uuid):
                    return {'error': "Device UUID already exists"}, 409
                else:

                    # Map the Creation DTO and the location_id of the URI to a new Device Model
                    new_device_model = DeviceModel.from_creation_dto(location_id, device_creation_request)

                    # Add the new device to the location
                    self.data_manager.add_device(location_id, new_device_model)

                    # Return the Location Header with the new Device UUID
                    return Response(status=201, headers={"Location": request.url+"/"+new_device_model.uuid})  # Force the No-Content Response
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

    def get(self, location_id: str) -> tuple[list[dict], int] | tuple[dict, int]:
        """ Retrieve all Devices in the specified Location"""

        # Check if the provided Location Id in the path is correct
        if self.data_manager.location_exists(location_id):

            # Check for query arguments
            parser = reqparse.RequestParser()
            parser.add_argument('type', location='args')

            # Use required=True to force the check for a specific field
            # parser.add_argument('locationId', location='args', required=True)
            args = parser.parse_args()

            # Retrieve filter value (None if the query argument is not provided)
            type_filter = args.get("type")

            # Retrieve the devices of the location, filtered by type if requested
            device_model_list = self.data_manager.get_device_list(location_id, type_filter)

            # Map each Device Model to a Device Entity Response and build a serializable device list
            device_list = [DeviceEntityResponse.from_model(device).__dict__ for device in device_model_list]

            # Return the filtered list
            return device_list, 200  # return data and 200 OK code

        else:
            return {'error': "Location Not Found !"}, 404
