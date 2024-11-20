# reminder.py
from datetime import datetime
from .location import Location
from .weather_data import WeatherData

class Reminder:
    def __init__(self):
        self.message = None

    def set_reminder_by_weather(self, data: WeatherData):
        # 根据天气数据设置提醒的逻辑
        if data.cur_temperature > 30:
            self.message = "今天天气炎热，请注意防暑"
        elif data.cur_weather == "暴雨":
            time = data.timestamp.hour
            self.message = "今天"+str(time)+"点以后有暴雨，出行请带好雨伞"
        elif data.cur_weather == "雷阵雨":
            time = data.timestamp.hour
            self.message = "今天"+str(time)+"点以后有雷阵雨，请注意安全"
        elif data.cur_weather == "中雨":
            time = data.timestamp.hour
            self.message = "今天"+str(time)+"点以后有中雨，请注意出行安全"

    def set_reminder_by_time(self, time: datetime):
        self.timestamp = time

