"""
Module: client.py
Description: This module defines the OpenWeatherMapClient class, which is responsible for fetching weather data
from the OpenWeatherMap API.

"""
import asyncio
import logging

import requests
from aiohttp import ClientSession
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class OpenWeatherMapClient:
    """
    OpenWeatherMapClient class is used to interact with the OpenWeatherMap API and fetch weather data for a given city.

    Attributes:
    - api_key (str): The API key used for authentication with the OpenWeatherMap API.
    - base_url (str): The base URL for OpenWeatherMap API requests.

    Methods:
    - get_weather(city): Fetches weather data for a given city.
    - get_city_info(city): Retrieves geographical information for a given city.
    - get_weather_data(lat, lon): Retrieves weather data for a specific geographical location.
    - parse_weather_data(weather_data): Parses raw weather data into a structured format.
    - get_wind_direction(deg): Converts wind degree into a human-readable direction.
    """

    def __init__(
        self, api_key=settings.OPEN_WEATHER_API_KEY, base_url=settings.BASE_API_URL
    ):
        """
        Constructor for OpenWeatherMapClient class.

        Parameters:
        - api_key (str): The API key used for authentication (default is the key from Django settings).
        - base_url (str): The base URL for API requests (default is the base URL from Django settings).
        """
        self.api_key = api_key
        self.base_url = base_url

    async def get_weather(self, city):
        """
        Fetches weather data for a given city.

        Parameters:
        - city (str): The name of the city for which weather data is requested.

        Returns:
        A dictionary containing weather information or an error message if the data retrieval fails.
        """
        lat, lon, country, state = await self.get_city_info(city)

        if not lat or not lon:
            logging.error(f"City not found for {city}")
            return {
                "error": True,
                "message": _("City not found"),
                "data": None,
            }

        weather_data = await self.get_weather_data(lat, lon)

        if not weather_data:
            logging.error(f"Failed to fetch weather data for {city}")
            return {
                "error": True,
                "message": _("Failed to fetch weather data."),
                "data": None,
            }

        parsed_weather_data = self.parse_weather_data(weather_data)
        logging.info(f"Weather data fetched successfully for {city}")
        return {
            "error": False,
            "message": _("weather data fetched successfully."),
            "data": parsed_weather_data,
        }

    async def get_city_info(self, city):
        """
        Retrieves geographical information for a given city.

        Parameters:
        - city (str): The name of the city for which geographical information is requested.

        Returns:
        A tuple containing latitude, longitude, country, and state information.
        """
        url = f"{self.base_url}geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                cities = await response.json()

        if not cities:
            return None, None, None, None

        city_data = cities[0]
        lat = city_data.get("lat")
        lon = city_data.get("lon")
        country = city_data.get("country")
        state = city_data.get("state")

        return lat, lon, country, state

    async def get_weather_data(self, lat, lon):
        """
        Retrieves weather data for a specific geographical location.

        Parameters:
        - lat (float): Latitude of the location.
        - lon (float): Longitude of the location.

        Returns:
        Raw weather data from the OpenWeatherMap API.
        """
        url = f"{self.base_url}data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={self.api_key}"
        async with ClientSession() as session:
            async with session.get(url) as response:
                weather_data = await response.json()

        if response.status != 200:
            return None

        return weather_data

    def parse_weather_data(self, weather_data):
        """
        Parses raw weather data obtained from the OpenWeatherMap API into a structured format.

        Parameters:
        - weather_data (dict): Raw weather data as a dictionary.

        Returns:
        A dictionary containing parsed weather information with the following keys:
        - "city" (str): The name of the city.
        - "temperature" (str): The temperature in degrees Celsius.
        - "min_temperature" (str): The minimum temperature in degrees Celsius.
        - "max_temperature" (str): The maximum temperature in degrees Celsius.
        - "humidity" (str): The humidity level as a percentage.
        - "pressure" (str): The atmospheric pressure in hPa (hectopascals).
        - "windSpeed" (str): The wind speed in meters per second.
        - "wind_direction" (str): The wind direction as a cardinal point (North, East, South, West).
        - "description" (str): A description of the weather conditions.

        Note:
        - If any key is missing in the weather_data dictionary, the corresponding value in the parsed_data
          dictionary will be set to None.
        - The wind_direction is determined based on the wind degree using the get_wind_direction method.
        """
        city_name = weather_data.get("name")
        temperature = weather_data["main"].get("temp")
        min_temp = weather_data["main"].get("temp_min")
        max_temp = weather_data["main"].get("temp_max")
        humidity = weather_data["main"].get("humidity")
        pressure = weather_data["main"].get("pressure")
        wind_speed = weather_data["wind"].get("speed")
        wind_direction = weather_data["wind"].get("deg")
        description = weather_data["weather"][0].get("description")

        parsed_data = {
            "city": city_name,
            "temperature": f"{temperature} °C",
            "min_temperature": f"{min_temp} °C",
            "max_temperature": f"{max_temp} °C",
            "humidity": f"{humidity}%",
            "pressure": f"{pressure} hPa",
            "windSpeed": f"{wind_speed} m/s",
            "wind_direction": self.get_wind_direction(wind_direction),
            "description": description,
        }

        return parsed_data

    def get_wind_direction(self, deg):
        """
        Converts wind degree into a human-readable direction.

        Parameters:
        - deg (float): Wind degree.

        Returns:
        A string representing the wind direction.
        """
        if deg > 45 and deg <= 135:
            return _("East")
        elif deg > 135 and deg <= 225:
            return _("South")
        elif deg > 225 and deg <= 315:
            return _("West")
        else:
            return _("North")
