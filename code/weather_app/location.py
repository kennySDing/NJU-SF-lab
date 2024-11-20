from typing import List
from .weather_forecast import WeatherForecast

class Location:
    def __init__(self, city_name: str, latitude: float, longitude: float):
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude
        self.weather_forecast = WeatherForecast()
