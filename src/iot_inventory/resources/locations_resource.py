from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from iot_inventory.dto.location_entity_response import LocationEntityResponse
from iot_inventory.dto.location_creation_request import LocationCreationRequest
from iot_inventory.model.location_model import LocationModel


class LocationsResource(Resource):
    """ Locations Resource Class """

    def __init__(self, **kwargs):
        """ Initialize the Locations Resource with the provided data manager """
        self.data_manager = kwargs['data_manager']

    def post(self):
        """ Create a new Location """
        try:

            # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)

            # Create a Location Creation Request Object
            location_creation_request = LocationCreationRequest(**json_data)

            # Check if the UUID already exists
            if location_creation_request.uuid in self.data_manager.location_dictionary:
                return {'error': "Location UUID already exists"}, 409  # return data and 200 OK code
            else:
                # Create a new Location Model
                new_location_model = LocationModel(location_creation_request.uuid,
                                                   location_creation_request.name,
                                                   location_creation_request.latitude,
                                                   location_creation_request.longitude)

                # Add the new Location to the Data Manager
                self.data_manager.add_location(new_location_model)

                # Return the Location UUID in the Location Header
                return Response(status=201, headers={"Location": request.url+"/"+new_location_model.uuid})  # Force the No-Content Response
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500

    def get(self):
        """ Get all Locations """

        # Iterate over the dictionary to build a serializable device list
        result_location_list = []

        # Iterate over the dictionary to build a serializable location list
        for location in self.data_manager.location_dictionary.values():

            # Iterate over the dictionary to build a serializable device id list
            device_id_list = []

            # Iterate over the dictionary to build a serializable device id list
            for device in location.device_dictionary.values():
                device_id_list.append(device.uuid)

            # Create a Location Entity Response Object
            location_entity_response = LocationEntityResponse(location.uuid,
                                                              location.name,
                                                              location.latitude,
                                                              location.longitude,
                                                              device_id_list)
            # Append the Location Entity Response to the List
            result_location_list.append(location_entity_response.__dict__)

        # Return the Location List
        return result_location_list, 200  # return data and 200 OK code