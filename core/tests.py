import unittest
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .client import OpenWeatherMapClient


class TestOpenWeatherMapClient(unittest.TestCase):
    async def asyncSetUp(self):
        self.api_key = settings.OPEN_WEATHER_API_KEY

    @patch("aiohttp.ClientSession.get")
    async def test_get_city_info_success(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"lat": 51.509865, "lon": -0.118092, "country": "GB", "state": "England"}
        ]

        weather_client = OpenWeatherMapClient(api_key=self.api_key)

        lat, lon, country, state = await weather_client.get_city_info("London")

        self.assertEqual(lat, 51.509865)
        self.assertEqual(lon, -0.118092)
        self.assertEqual(country, "GB")
        self.assertEqual(state, "England")

    @patch("aiohttp.ClientSession.get")
    async def test_get_city_info_invalid(self, mock_get):
        mock_get.return_value.json.return_value = []

        weather_client = OpenWeatherMapClient(api_key=self.api_key)

        result = await weather_client.get_city_info("rendomx")

        self.assertIsNone(result[0])
        self.assertIsNone(result[1])
        self.assertIsNone(result[2])
        self.assertIsNone(result[3])

    @patch("aiohttp.ClientSession.get")
    async def test_get_weather_data_success(self, mock_get):
        mock_get.return_value.status = 200
        mock_get.return_value.json.return_value = {"main": {"temp": 25.5}}

        weather_client = OpenWeatherMapClient(api_key=self.api_key)

        result = await weather_client.get_weather_data(51.509865, -0.118092)

        self.assertIsNotNone(result)
        self.assertEqual(result["main"]["temp"], 25.5)

    @patch("aiohttp.ClientSession.get")
    async def test_get_weather_data_failure(self, mock_get):
        mock_get.return_value.status = 404

        weather_client = OpenWeatherMapClient(api_key=self.api_key)

        result = await weather_client.get_weather_data(51.509865, -0.118092)

        self.assertIsNone(result)


def get_city_url(city):
    return reverse("core:weather-api", kwargs={"city": city})


# class WeatherAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#     @patch("django.core.cache.cache.get", return_value=None)
#     def test_get_weather_data(self, mock_cache_get):
#         # avoid connecting to memcached
#         with patch("django.core.cache.cache.set", new_callable=MagicMock) as mock_cache_set:
#             response = self.client.get(get_city_url("London"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("city", response.data)
#         self.assertIn("temperature", response.data)
#         self.assertIn("wind_direction", response.data)
#
#     @patch("django.core.cache.cache.get", return_value=None)
#     def test_get_weather_data_invalid_city(self, mock_cache_get):
#         with patch("django.core.cache.cache.set", new_callable=MagicMock) as mock_cache_set:
#             response = self.client.get(get_city_url("..."))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertIn("message", response.data)
