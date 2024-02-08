from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    City = serializers.CharField(max_length=100)
    Temperature = serializers.CharField(max_length=100)
    MinTemperature = serializers.CharField(max_length=100)
    MaxTemperature = serializers.CharField(max_length=100)
    Humidity = serializers.CharField(max_length=100)
    Pressure = serializers.CharField(max_length=100)
    WindSpeed = serializers.CharField(max_length=100)
    WindDirection = serializers.CharField(max_length=100)
    Description = serializers.CharField(max_length=255)
