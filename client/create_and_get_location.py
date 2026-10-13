import requests

import requests

# Target API URL
api_url = "http://127.0.0.1:7070/api/iot/inventory/location"

# Define Request Body as Python dictionary
request_dictionary = {
    "uuid": "l112",
    "name": "PythonTestBuilding",
    "latitude": 48.412321,
    "longitude": 10.533423211
}

# Send the POST Request with the body serialized as Json (Internally managed by the library)
response = requests.post(api_url, json=request_dictionary)

# Read Status code and Location Header
response_code = response.status_code

# Read Status code and Location Header
if response_code == 201 and "Location" in response.headers:

    # Read Location Header
    location_header = response.headers["Location"]
    print(f'HTTP Response Code: {response.status_code} - Buffer Body: {response.content} - Location Header: {location_header}')

    # Read the Location Resource
    get_api_url = location_header

    # Send the GET Request to the Location Resource
    response = requests.get(get_api_url)

    # Parse the Json Body
    json_response = response.json()

    print("Reading the new created Location Resource ...")
    print(f'HTTP Response Code: {response.status_code} - Json Parsed Body {json_response}')
else:
    print(f'Error creating the Location ! Code: {response_code} and Reason: {str(response.content, "UTF-8").strip()}')