# Python - IoT Inventory - Demo RESTful HTTP API

This project shows a demo implementation of a simple IoT device and location inventory through 
an HTTP RESTful API.

The structure of the playground is the following:

- [Libraries, Frameworks, and Dependencies](#libraries-frameworks-and-dependencies)
- [Modeled REST Resources](#modeled-rest-resources)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
- [Postman Collection](#postman-collection)

## Libraries, Frameworks, and Dependencies

The implementation is based on the following Python Frameworks 

- Flask: https://flask.palletsprojects.com/en/2.0.x/
- Flask RESTful: https://flask-restful.readthedocs.io/en/latest/index.html

APIs are exposed through a configurable port (7070) and accessible locally at: http://127.0.0.1:7070/api/iot/

The project is managed with [uv](https://docs.astral.sh/uv/). Dependencies are declared in `pyproject.toml`,
locked in `uv.lock`, and the Python version (3.12) is pinned in `.python-version`.

- Server dependencies: `flask`, `flask-restful`
- Client dependencies (dependency group `client`, installed by default): `requests`

Install uv (if needed) following the [official instructions](https://docs.astral.sh/uv/getting-started/installation/), e.g.:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, from the project root, create the virtual environment (`.venv`) and install all the dependencies with:

```bash
uv sync
```

uv automatically downloads the required Python version if it is not available on your machine.

In PyCharm, you can select the existing `.venv` interpreter or add a new "uv" interpreter from the interpreter settings.

### Using pip (alternative)

The `requirements.txt` file is **generated** from `uv.lock` and is kept only for pip-based workflows:

```bash
pip install -r requirements.txt
```

Do not edit it manually. After changing the dependencies, regenerate it with:

```bash
uv export --no-hashes --no-dev --group client -o requirements.txt
```

## Modeled REST Resources

- **/location**
  - _GET_: Returns the list of available locations
  - _POST_: Handles the creation of a new location

- **/location/<location_id>**
  - _GET_: Returns the target location with the specified `location_id`
  - _PUT_: Updates the target location with the specified `location_id`
  - _DELETE_: Deletes the target location with the specified `location_id`

- **/location/<location_id>/device**
  - _GET_: Returns the list of devices for the specified `location_id`
  - _POST_: Creates a new device for the specified `location_id`

- **/location/<location_id>/device/<device_id>**
  - _GET_: Returns the target device with the specified `device_id` associated with the specified `location_id`
  - _PUT_: Updates the target device with the specified `device_id` associated with the specified `location_id`
  - _DELETE_: Deletes the target device with the specified `device_id` associated with the specified `location_id`

A string like `<location_id>` or `<device_id>` is a placeholder for the actual location or device identifier.
In the current implementation device's data (e.g., temperature values or actuator status) are not handled and they are out of the scope of the demo inventory.

## Project Structure

The project follows the `src` layout: the server code is the `iot_inventory` package in `src/`,
while the clients are standalone example scripts outside the package.

```
python-http-api-playground/
├── pyproject.toml          # Project metadata, dependencies and entry points
├── uv.lock                 # Locked dependency versions (managed by uv)
├── requirements.txt        # Generated from uv.lock for pip users
├── src/iot_inventory/      # Server application package
│   ├── __main__.py         # Enables: python -m iot_inventory
│   ├── api_server.py       # create_server_app() factory and main() entry point
│   ├── dto/
│   ├── model/
│   ├── persistence/
│   └── resources/
├── client/                 # Standalone HTTP client examples (requests)
├── tests/                  # Test scripts
└── postman/                # Postman collection
```

- **Server Application** (`src/iot_inventory`):
  - _api_server.py_: The main entry point of the project. It contains:
    - `create_server_app()`: the Flask App Factory that creates the application and registers the API resources. Importing the module has no side effects and each call returns a new, independent app (useful for testing with `app.test_client()`).
    - `load_demo_data()`: adds a demo location and a demo device to the Data Manager.
    - `main()`: loads the demo data, creates the app and starts the server on port 7070.
- **Resources**: Contains the API resources for the locations and devices. Detailed in the following files:
  - _locations_resource.py_: Contains the LocationsResource class that handles the list of devices resource.
  - _location_resource.py_: Contains the LocationResource class that handles the device resources.
  - _devices_resource.py_: Contains the DevicesResource class that handles the list of devices resource.
  - _device_resource.py_: Contains the DeviceResource class that handles the device resources.
- **Models**: Contains the data models for the locations and devices. Detailed in the following files:
  - _location_model.py_: Contains the Location class that represents a location.
  - _device_model.py_: Contains the Device class that represents a device.
- **DTO**: Contains the Data Transfer Objects (DTOs) for the locations and devices. Detailed in the following files:
  - _device_creation_request.py_: Contains the DeviceCreationRequest class that represents the request to create a device.
  - _device_update_request.py_: Contains the DeviceUpdateRequest class that represents the request to update a device. 
  - _location_creation_request.py_: Contains the LocationCreationRequest class that represents the request to create a location. 
  - _location_entity_response.py_: Contains the LocationEntityResponse class that represents the response of a location entity. 
  - _location_update_request.py_: Contains the LocationUpdateRequest class that represents the request to update a location.
- **Persistence**: Contains the data access layer for the locations and devices. Detailed in the following file:
  - _data_manager.py_: Contains the DataManager class that handles the data access layer for the locations and devices.
- **Clients**: Contains the client to interact with the API. Detailed in the following file:
  - _create_and_get_location.py_: Implements the client to create a location and get the list of locations through the implemented API.
  - _create_location.py_: Implements the client to create a location through the implemented API.
  - _delete_location.py_: Implements the client to delete a location through the implemented API.
  - _get_location_list.py_: Implements the client to get the list of locations through the implemented API.
  - _get_single_location.py_: Implements the client to get a single location through the implemented API.
  - _update_location.py_: Implements the client to update a location through the implemented API.

## Running the Project

The server is exposed as a command (`iot-inventory-server`) declared in the `[project.scripts]` section
of `pyproject.toml`. From the project root run:

```bash
uv run iot-inventory-server
```

Alternatively, you can run it as a module or execute the file directly:

```bash
uv run python -m iot_inventory
uv run src/iot_inventory/api_server.py
```

The server will start and expose the API resources through the configured port by default (7070).

Since the app is built through the `create_server_app()` factory, it can also be started with the Flask CLI
(note that in this case the demo data are not loaded):

```bash
uv run flask --app "iot_inventory.api_server:create_server_app()" run --port 7070
```

With the server running, you can execute any of the clients in another terminal, e.g.:

```bash
uv run client/create_location.py
uv run client/get_location_list.py
```

## Postman Collection

In the `postman` folder, you can find a Postman collection that contains the requests to interact with the implemented API.
You can import the collection into Postman and run the requests to interact with the API.
  