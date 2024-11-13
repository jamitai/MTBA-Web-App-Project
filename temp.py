# import json
# import os
# import pprint
# from dotenv import load_dotenv
# from urllib import request, error, parse

# # Load environment variables
# load_dotenv()
# # Get API keys from environment variables
# OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
# MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
# MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
# OPEN_WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ##print("open_weather_base_url:", OPEN_WEATHER_BASE_URL)
# # A little bit of scaffolding if you want to use it
# def get_json(url: str) -> dict:
#     """
#     Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
#     Both get_lat_lng() and get_nearest_station() might need to use this function.
#     """
#     with request.urlopen(url) as response:
#         response_text = response.read().decode("utf-8")
#         response_data = json.loads(response_text)
#         return response_data
#     pass


# def get_weather(latitude: str, longitude: str) -> dict:
#     """
#     Given latitude and longitude strings, return a dictionary with the current weather information including temperature,
#     weather description, and humidity.
#     """
#     url = f"{OPEN_WEATHER_BASE_URL}?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
#     print(url)
#     weather_data = get_json(url) 
#     # Extract relevant weather information
#     temperature = weather_data["main"]["temp"]
#     weather_description = weather_data["weather"][0]["description"]
#     humidity = weather_data["main"]["humidity"]
#     return {
#         "temperature": temperature,
#         "weather_description": weather_description,
#         "humidity": humidity,
#     }


# def main():
#     """
#     You should test all the above functions here
#     """
#     result = get_weather("42.352413", "-71.110667")
#     print("Current weather:")
#     print(f"Temperature: {result['weather']['temperature']}°F")
#     print(f"Condition: {result['weather']['weather_description'].capitalize()}")
#     print(f"Humidity: {result['weather']['humidity']}%")

# if __name__ == "__main__":
#     main()
