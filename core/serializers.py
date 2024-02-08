from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    temperature = serializers.CharField(max_length=100)
    min_temperature = serializers.CharField(max_length=100)
    max_temperature = serializers.CharField(max_length=100)
    humidity = serializers.CharField(max_length=100)
    pressure = serializers.CharField(max_length=100)
    windSpeed = serializers.CharField(max_length=100)
    wind_direction = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
