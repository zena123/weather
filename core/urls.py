from django.urls import path

from .views import WeatherAPIView

app_name = "core"

urlpatterns = [
    path('weather/<str:city>/', WeatherAPIView.as_view(), name='weather-api'),

]
