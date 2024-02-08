from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response

from .client import OpenWeatherMapClient
from .serializers import WeatherSerializer


@method_decorator(cache_page(60 * 5), name='dispatch')
class WeatherAPIView(generics.RetrieveAPIView):
    serializer_class = WeatherSerializer

    def get(self, request, *args, **kwargs):
        city = self.kwargs.get("city")
        client = OpenWeatherMapClient()

        weather_data = client.get_weather(city)

        if weather_data["error"]:
            print(status.HTTP_404_NOT_FOUND)
            return Response(data=weather_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(weather_data["data"])
        return Response(serializer.data, status=status.HTTP_200_OK)
