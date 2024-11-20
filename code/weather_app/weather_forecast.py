from typing import List
from .weather_data import WeatherData
from datetime import datetime, timedelta
import random
import json
import requests
from datetime import datetime


class WeatherForecast:
    def __init__(self):
        self.weather_data_hour: List[WeatherData]=[]
        self.weather_data_day: List[WeatherData]=[]

    def judge_pollution_level(self, pollution_level: float) -> str:
        if pollution_level < 50:
            return "优"
        elif pollution_level < 100:
            return "良"
        elif pollution_level < 150:
            return "轻度污染"
        elif pollution_level < 200:
            return "中度污染"
        elif pollution_level < 300:
            return "重度污染"
        else:
            return "严重污染"

    def judge_windSPeed(self, wind_speed: str) -> str:
        if wind_speed == "5 km/h":
            return "1级风力"
        elif wind_speed == "10 km/h":
            return "2级风力"
        elif wind_speed == "15 km/h":
            return "3级风力"
        elif wind_speed == "20 km/h":
            return "4级风力"
        elif wind_speed == "25 km/h":
            return "5级风力"
        else:
            return "6级风力"
    
    def judge_visibility(self, visibility: float) -> str:
        if visibility < 1:
            return "极差"
        elif visibility < 3:
            return "很差"
        elif visibility < 5:
            return "较差"
        elif visibility < 10:
            return "一般"
        else:
            return "良好"
    
    def get_weather_data_by_day(self,  city_name, num_days) -> List[WeatherData]:
        
        daily_weather = []
        base_date = datetime.now()  # 基准日期，设定在中午12点

        wind_directions = ["北风", "东北风", "东风", "东南风", "南风", "西南风", "西风", "西北风"]
        wind_speeds = ["5 km/h", "10 km/h", "15 km/h", "20 km/h", "25 km/h", "30 km/h"]
        weather_condition = ["晴","多云","小雨","中雨","暴雨","雷阵雨","阴"]
        for day in range(num_days):
            
            high_temperature = round(random.uniform(20, 35), 1)  # 温度范围：
            low_temperature = round(random.uniform(10, 20), 1)  
            cur_temperature = round(random.uniform(low_temperature, high_temperature), 1)
            cur_weather = random.choice(weather_condition)
            humidity = random.randint(20, 100)               # 湿度范围：20% 到 100%
            wind_direction = random.choice(wind_directions)
            wind_speed = random.choice(wind_speeds)
            probability_of_rain = random.randint(0, 100)     # 降雨概率范围：0% 到 100%
            pollution_level = round(random.uniform(0, 50), 1)  # 空气污染指数范围：0 到 500
            visibility = round(random.uniform(1, 20), 1)         # 范围：1km 到 20km

            timestamp = base_date + timedelta(days=day)
            city = city_name

            weather = WeatherData(
                cur_temperature=cur_temperature,
                high_temperature=high_temperature,
                low_temperature=low_temperature,
                cur_weather=cur_weather,
                humidity=humidity,
                wind_direction=wind_direction,
                wind_speed=wind_speed,
                probability_of_rain=probability_of_rain,
                pollution_level=pollution_level,
                visibility=visibility,
                timestamp=timestamp,
                city=city
            )
            daily_weather.append(weather)
            
        self.weather_data_day = daily_weather
        return

    def get_weather_data_by_hour(self, city_name) -> List[WeatherData]:
        # 实现按小时获取天气数据的逻辑
        hour_weather = []
        base_date = datetime.now()
        wind_directions = ["北风", "东北风", "东风", "东南风", "南风", "西南风", "西风", "西北风"]
        wind_speeds = ["5 km/h", "10 km/h", "15 km/h", "20 km/h", "25 km/h", "30 km/h"]
        weather_condition = ["晴","多云","小雨","中雨","暴雨","雷阵雨","阴"]
        for hour in range(24):
            high_temperature = round(random.uniform(20, 35), 1)
            low_temperature = round(random.uniform(10, 20), 1)
            cur_temperature = round(random.uniform(low_temperature, high_temperature), 1)
            cur_weather = random.choice(weather_condition)
            humidity = random.randint(20, 100)
            wind_direction = random.choice(wind_directions)
            wind_speed = random.choice(wind_speeds)
            probability_of_rain = random.randint(0, 100)
            pollution_level = round(random.uniform(0, 100), 1)
            visibility = round(random.uniform(1, 20), 1)

            timestamp = base_date + timedelta(hours=hour)
            city = city_name

            weather = WeatherData(
                cur_temperature=cur_temperature,
                high_temperature=high_temperature,
                low_temperature=low_temperature,
                cur_weather=cur_weather,
                humidity=humidity,
                wind_direction=wind_direction,
                wind_speed=wind_speed,
                probability_of_rain=probability_of_rain,
                pollution_level=pollution_level,
                visibility=visibility,
                timestamp=timestamp,
                city=city
            )
            hour_weather.append(weather)
        self.weather_data_hour = hour_weather

        pass