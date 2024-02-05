import requests
from datetime import datetime
from django.utils.translation import gettext_lazy as _

from django.conf import settings


class OpenWeatherMapClient:
    def __init__(self, api_key=settings.OPEN_WEATHER_API_KEY):
        self.api_key = api_key

    def get_weather(self, city):
        lat, lon, country, state = self.get_city_info(city)

        if not lat or not lon:
            # TODO: log error and request
            return {
                "error": True,
                "message": _("City not found"),
                "data": None,
            }

        weather_data = self.get_weather_data(lat, lon)

        if not weather_data:
            # TODO: log error and request
            return {
                "error": True,
                "message": _("Failed to fetch weather data."),
                "data": None,
            }

        parsed_weather_data = self.parse_weather_data(weather_data)
        return {
            "error": True,
            "message": _("Failed to fetch weather data."),
            "data": parsed_weather_data,
        }

    def get_city_info(self, city):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
        response = requests.get(url)
        cities = response.json()

        if not cities:
            return None, None, None, None

        city_data = cities[0]
        lat = city_data.get("lat")
        lon = city_data.get("lon")
        country = city_data.get("country")
        state = city_data.get("state")

        return lat, lon, country, state

    def get_weather_data(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={self.api_key}"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200:
            return None

        return weather_data

    def parse_weather_data(self, weather_data):
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
            "City": city_name,
            "Temperature": f"{temperature} °C",
            "Min Temperature": f"{min_temp} °C",
            "Max Temperature": f"{max_temp} °C",
            "Humidity": f"{humidity}%",
            "Pressure": f"{pressure} hPa",
            "Wind Speed": f"{wind_speed} m/s",
            "Wind Direction": self.get_wind_direction(wind_direction),
            "Description": description
        }

        return parsed_data

    def get_wind_direction(self, deg):
        if deg > 45 and deg <= 135:
            return "East"
        elif deg > 135 and deg <= 225:
            return "South"
        elif deg > 225 and deg <= 315:
            return "West"
        else:
            return "North"