from typing import List, Optional
from .weather_data import WeatherData
from .user import User
from .settings import Settings
from .theme import Theme
from .location import Location
from .weather_forecast import WeatherForecast

class Database:
    def __init__(self):
        self.themes: List[Theme] = []
        self.weather_data: List[WeatherData] = []
        self.users: List[User] = []