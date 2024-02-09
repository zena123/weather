# views.py
import asyncio

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import WeatherSerializer
from .client import OpenWeatherMapClient

@method_decorator(cache_page(settings.CACHE_SECONDS), name='dispatch')
class WeatherAPIView(RetrieveAPIView):
    serializer_class = WeatherSerializer
    async def fetch_weather_data(self, city):
        client = OpenWeatherMapClient()
        return await client.get_weather(city)

    def get(self, request, *args, **kwargs):
        city = self.kwargs.get('city')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            weather_data = loop.run_until_complete(self.fetch_weather_data(city))

            if weather_data.get('error'):
                return Response(weather_data, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(weather_data["data"])

            return Response(serializer.data, status=status.HTTP_200_OK)

        finally:
            loop.close()
