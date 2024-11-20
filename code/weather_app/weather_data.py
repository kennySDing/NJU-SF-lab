from datetime import datetime

class WeatherData:
    def __init__(self, cur_temperature:float, high_temperature: float, low_temperature:float, cur_weather:str, humidity: float, wind_direction: str,
                 wind_speed: str, probability_of_rain: int, pollution_level: float,
                 visibility: float, timestamp: datetime, city:str):
        self.cur_temperature = cur_temperature
        self.high_temperature = high_temperature
        self.low_temperature = low_temperature
        self.cur_weather = cur_weather
        self.humidity = humidity
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        self.probability_of_rain = probability_of_rain
        self.pollution_level = pollution_level
        self.visibility = visibility
        self.timestamp = timestamp
        self.city = city
    def read_weather_data(self):
        # 实现读取天气数据的逻辑
        pass