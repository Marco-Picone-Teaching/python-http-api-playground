from flask import Flask
from flask_restful import Api
from iot_inventory.resources.device_resource import DeviceResource
from iot_inventory.resources.devices_resource import DevicesResource
from iot_inventory.resources.locations_resource import LocationsResource
from iot_inventory.resources.location_resource import LocationResource
from iot_inventory.persistence.data_manager import DataManager
from iot_inventory.model.location_model import LocationModel
from iot_inventory.model.device_model import DeviceModel

# Define API Endpoint Prefix
ENDPOINT_PREFIX = "/api/iot/inventory"

# Default Host and Port of the HTTP Server
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 7070


def create_server_app(data_manager=None):
    """
    Create and configure the Flask App with the RESTful API resources (App Factory pattern).
    If no Data Manager is provided, a new empty one is created.
    """

    # Create Data Manager to handle the data of locations and devices
    if data_manager is None:
        data_manager = DataManager()

    # Create Flask App
    app = Flask(__name__)

    # Create RESTful API
    api = Api(app)

    # Add Locations Resource to handle the list of locations
    api.add_resource(LocationsResource, ENDPOINT_PREFIX + '/location',
                     resource_class_kwargs={'data_manager': data_manager},
                     endpoint="locations",
                     methods=['GET', 'POST'])

    # Add Location Resource to handle a specific location by its id
    api.add_resource(LocationResource, ENDPOINT_PREFIX + '/location/<string:location_id>',
                     resource_class_kwargs={'data_manager': data_manager},
                     endpoint='location',
                     methods=['GET', 'PUT', 'DELETE'])

    # Add Devices Resource to handle the list of devices for a specific location
    api.add_resource(DevicesResource, ENDPOINT_PREFIX + '/location/<string:location_id>/device',
                     resource_class_kwargs={'data_manager': data_manager},
                     endpoint="devices",
                     methods=['GET', 'POST'])

    # Add Device Resource to handle a specific device by its id and the associated location id
    api.add_resource(DeviceResource, ENDPOINT_PREFIX + '/location/<string:location_id>/device/<string:device_id>',
                     resource_class_kwargs={'data_manager': data_manager},
                     endpoint='device',
                     methods=['GET', 'PUT', 'DELETE'])

    return app


def load_demo_data(data_manager):
    """ Create Demo Data for the API in order to have some data to work with """

    # Demo Location
    demo_location = LocationModel("l0001",
                                  "TestBuilding",
                                  48.312321,
                                  10.433423211)

    # Add New Location
    data_manager.add_location(demo_location)

    # Demo Device for the previous location
    demo_device = DeviceModel("d0001",
                              "demo-device",
                              demo_location.uuid,
                              DeviceModel.DEVICE_TYPE_DEFAULT,
                              "ACME Inc",
                              "0.0.1beta",
                              48.312321,
                              10.433423211)

    # Add New Device
    data_manager.add_device(demo_location.uuid, demo_device)


def main():
    """ Create demo data and start the Flask App (entry point of the project) """

    # Create Data Manager and fill it with the demo data
    data_manager = DataManager()
    load_demo_data(data_manager)

    # Create the Flask App using the populated Data Manager
    app = create_server_app(data_manager)

    print("Starting HTTP RESTful API Server ...")

    # Run the Flask App
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)


# Start the Flask App
if __name__ == '__main__':
    main()
