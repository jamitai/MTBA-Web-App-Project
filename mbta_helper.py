import json
import os
import pprint
from dotenv import load_dotenv
from urllib import request, error, parse

# Load environment variables
load_dotenv()


# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        response_data = json.loads(response_text)
        return response_data
    pass


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    place_name = place_name.replace(" ", "%20")  # Replace spaces with %20
    url = f"{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}&types=poi"
    json_data = get_json(url)
    long, lat = json_data["features"][0]["center"]
    return (str(lat), str(long))


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """

    # Parameters for the request
    params = {
        "sort": "distance",
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
    }

    # Encode parameters for URL
    encoded_params = parse.urlencode(params)
    url = f"{MBTA_BASE_URL}?{encoded_params}"

    try:
        # Create request object with headers
        req = request.Request(
            url, headers={"x-api-key": MBTA_API_KEY, "Accept": "application/json"}
        )

        # Make the request
        with request.urlopen(req) as response:
            # Read and decode the response
            mbta_data = response.read().decode("utf-8")
            mbta_json = json.loads(mbta_data)
    except error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return None
    except error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

    # Grab the station name and wheelchair accessibility
    station_name = mbta_json["data"][0]["attributes"]["name"]
    wheelchair_accessible = (
        mbta_json["data"][0]["attributes"]["wheelchair_boarding"] == 1
    )
    return (station_name, wheelchair_accessible)


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    place_coords = get_lat_lng(place_name)
    lat, long = place_coords
    return get_nearest_station(lat, long)


def main():
    """
    You should test all the above functions here
    """
    query = "Boston University"
    print(find_stop_near(query))


if __name__ == "__main__":
    main()