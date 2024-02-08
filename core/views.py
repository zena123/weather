from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .client import OpenWeatherMapClient
from .serializers import WeatherSerializer


class WeatherAPIView(generics.RetrieveAPIView):
    serializer_class = WeatherSerializer

    def get(self, request, *args, **kwargs):
        city = self.kwargs.get('city')
        client = OpenWeatherMapClient()

        weather_data = client.get_weather(city)

        if weather_data["error"]:
            print(status.HTTP_404_NOT_FOUND)
            return Response(data=weather_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(weather_data["data"])
        return Response(serializer.data, status=status.HTTP_200_OK)
