import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from weather_app.location import Location
from weather_app.theme import Theme
from weather_app.settings import Settings
from weather_app.user import User
from weather_app.reminder import Reminder
from weather_app.database import Database

class MainScreen:
    def __init__(self, window):
        self.window = window
        self.window.title('天气App')
        self.window.geometry('400x600')
        # 初始化数据库和用户
        self.init_db()
        self.current_user = None
        # 创建 Canvas 并填充整个窗口
        self.canvas = tk.Canvas(self.window, width=400, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.Images = []

        self.weather_photo ={}
        self.weather_photo["晴"] = "pic/sun.png"
        self.weather_photo["多云"] = "pic/cloud.png"
        self.weather_photo["阴"] = "pic/cloudy.png"
        self.weather_photo["小雨"] = "pic/little_rain.png"
        self.weather_photo["中雨"] = "pic/mid_rain.png"
        self.weather_photo["暴雨"] = "pic/big_rain.png"
        self.weather_photo["雷阵雨"] = "pic/thunder.png"

        self.cur_screen = "Login"

        self.word_color ={}
        self.word_color[True] = "white"
        self.word_color[False] = "black"

        self.bg_color ={}
        self.bg_color[True] = "pic/night.jpg"
        self.bg_color[False] = "pic/sky.png"

        #加载城市列表
        self.city_list = self.load_cities("city/chinese_cities.json")
        # 显示登录界面
        self.show_login()

    def init_db(self):
        self.db = Database()
        theme = Theme('Default', 'Light', 10)  # 默认主题
        self.db.themes.append(theme)
        self.settings = Settings(False, theme)
        
        location = Location('南京', 32.04, 118.78)
        user = User('root', '123', self.settings, location, [])

        shanghai = Location('上海', 31.23, 121.47)
        beijing = Location('北京', 39.91, 116.39)
        suzhou = Location('苏州', 31.30, 120.62)
        user.favorite_locations.extend([shanghai, beijing, suzhou])
        self.db.users.append(user)
    
    def load_cities(self, json_file):
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                cities = json.load(file)
                # 使用集合存储小写城市名称，便于高效搜索和不区分大小写
                
                return cities
        except FileNotFoundError:
            print(f"错误：无法找到文件 '{json_file}'。请确保文件存在。")
            return set()
        except json.JSONDecodeError:
            print(f"错误：文件 '{json_file}' 不是有效的 JSON 格式。")
            return set()
        except Exception as e:
            print(f"发生错误：{e}")
            return set()

    def show_picture(self, pic, width, height, x, y):
        try:
            image = Image.open(pic)
            image = image.resize((width,height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(x, y, anchor='nw', image=photo)
            self.Images.append(photo)

        except Exception as e:
            print("无法加载图片", e)

    
    def show_login(self):
        self.cur_screen = "Login"
        # 清空 Canvas
        self.canvas.delete("all")
        self.show_picture("pic/sky.png", 400, 600, 0, 0)
        
        
        self.canvas.create_text(200, 80, text="欢迎使用天气应用", font=("微软雅黑", 20), fill="black")
        
        # 创建用户标签和输入框
        self.canvas.create_text(80, 150, text="账号:", font=("微软雅黑", 12), fill="black", anchor='w')
        self.user_id_entry = tk.Entry(self.window)
        self.canvas.create_window(200, 150, window=self.user_id_entry, width=150)
        
        # 创建密码标签和输入框
        self.canvas.create_text(80, 200, text="密码:", font=("微软雅黑", 12), fill="black", anchor='w')
        self.password_entry = tk.Entry(self.window, show="*")
        self.canvas.create_window(200, 200, window=self.password_entry, width=150)
        
        # 创建登录按钮
        login_button = tk.Button(self.window, text="登录",command=self.login)
        self.canvas.create_window(200, 250, window=login_button, width=100, height=30)
        
        # 创建注册按钮
        register_button = tk.Button(self.window, text="注册", command=self.show_register)
        self.canvas.create_window(200, 300, window=register_button, width=100, height=30)
    
    def show_register(self):
        self.cur_screen = "Register"
        # 清空 Canvas
        self.canvas.delete("all")
        self.show_picture("pic/sky.png", 400, 600, 0, 0)
        
        self.canvas.create_text(200, 80, text="注册", font=("微软雅黑", 20), fill="black")
        
        # 创建新用户ID标签和输入框
        self.canvas.create_text(75, 150, text="新用户", font=("微软雅黑", 12), fill="black", anchor='w')
        self.new_user_id_entry = tk.Entry(self.window)
        self.canvas.create_window(200, 150, window=self.new_user_id_entry, width=150)
        
        # 创建新密码标签和输入框
        self.canvas.create_text(75, 200, text="新密码:", font=("微软雅黑", 12), fill="black", anchor='w')
        self.new_password_entry = tk.Entry(self.window, show="*")
        self.canvas.create_window(200, 200, window=self.new_password_entry, width=150)
        
        # 创建提交按钮
        submit_button = tk.Button(self.window, text="提交", command=self.register)
        self.canvas.create_window(200, 250, window=submit_button, width=100, height=30)
        
        # 创建返回登录按钮
        back_button = tk.Button(self.window, text="返回登录", command=self.show_login)
        self.canvas.create_window(200, 300, window=back_button, width=100, height=30)
    
    def show_main_screen(self):
        self.cur_screen = "MainScreen"
        

        # 清空 Canvas
        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)
        self.show_picture("pic/rectangle.png", 390, 130, 5, 180)
        self.show_picture("pic/rectangle.png", 390, 170, 5, 325)
        cur_location = "当前位置"
        self.canvas.create_text(200, 20, text=cur_location, font=("微软雅黑", 10, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        cur_city = self.current_user.current_location.city_name
        self.canvas.create_text(200, 50, text=cur_city, font=("微软雅黑", 20), fill=self.word_color[self.current_user.settings.night_mode])

        
        # 获取两周的天气预报
        #先从database中找有没有缓存的数据
        num_days = 14
        city=self.current_user.current_location
        exist = False
        for day in range(num_days):
            exist = False
            for data in self.db.weather_data:
                if data.city == city.city_name and data.timestamp.date() == (datetime.now()+timedelta(days=day)).date():
                    exist = True
                    break
            if not exist:
                break
        #如果不存在，调用API获取数据
        if not exist:
            city.weather_forecast.get_weather_data_by_day(city.city_name, num_days)
            for i in range(num_days):
                self.db.weather_data.append(city.weather_forecast.weather_data_day[i])        
        else:
            city.weather_forecast.weather_data_day = []
            for i in range(num_days):
                for data in self.db.weather_data:
                    if data.city == city.city_name and data.timestamp.date() == (datetime.now()+timedelta(days=i)).date():
                        city.weather_forecast.weather_data_day.append(data)
            
        cur_temp = city.weather_forecast.weather_data_day[0].cur_temperature
        self.canvas.create_text(200, 80, text=str(cur_temp)+"°", font=("微软雅黑", 20), fill=self.word_color[self.current_user.settings.night_mode])
        high_temp = city.weather_forecast.weather_data_day[0].high_temperature
        self.canvas.create_text(150, 110, text="最高: "+str(high_temp)+"°", font=("微软雅黑", 12,"bold"), fill=self.word_color[self.current_user.settings.night_mode])
        low_temp = city.weather_forecast.weather_data_day[0].low_temperature
        self.canvas.create_text(250, 110, text="最低: "+str(low_temp)+"°", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        cur_weather = city.weather_forecast.weather_data_day[0].cur_weather
        self.canvas.create_text(200, 140, text=cur_weather, font=("微软雅黑", 16, "bold"), fill=self.word_color[self.current_user.settings.night_mode])

        week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i in range(4):
            if i == 0:
                date = "今天"
            elif i == 1:
                date = "明天"
            else:
                date = week_list[city.weather_forecast.weather_data_day[i].timestamp.weekday()]
            
            high_temp = city.weather_forecast.weather_data_day[i].high_temperature
            low_temp = city.weather_forecast.weather_data_day[i].low_temperature
            cur_weather = city.weather_forecast.weather_data_day[i].cur_weather

            self.canvas.create_text(50, 350+40*i, text=date, font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            weather_photo = self.weather_photo[cur_weather]
            self.show_picture(weather_photo, 30, 30, 100, 335+40*i)
            self.canvas.create_text(280, 350+40*i, text=str(low_temp)+"°"+"————"+
                                    str(high_temp)+"°", font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            if (i != 0):
                self.show_picture("pic/line_white.png", 370, 2, 15, 330+40*i)
        

        #获取一天内的天气预报
        num_hours = 24
        city=self.current_user.current_location
        exist = False
        for hour in range(num_hours):
            exist = False
            for data in self.db.weather_data:
                if data.city == city.city_name and data.timestamp.hour == (datetime.now()+timedelta(hours=hour)).hour:
                    exist = True
                    break
            if not exist:
                break
        #如果不存在，调用API获取数据
        if not exist:
            city.weather_forecast.get_weather_data_by_hour(city.city_name)
            for i in range(24):
                self.db.weather_data.append(city.weather_forecast.weather_data_hour[i])   
        else:
            city.weather_forecast.weather_data_hour = []
            for i in range(24):
                for data in self.db.weather_data:
                    if data.city == city.city_name and data.timestamp.hour== (datetime.now()+timedelta(hours=i)).hour:
                        city.weather_forecast.weather_data_hour.append(data)
                        break

        for i in range(5):
            if i == 0 :
                time = "现在"
            else :
                time = city.weather_forecast.weather_data_hour[i].timestamp.strftime("%H:%M")
            if time == "现在":
                temp = city.weather_forecast.weather_data_day[i].cur_temperature
            else:
                temp = city.weather_forecast.weather_data_hour[i].cur_temperature
            weather = city.weather_forecast.weather_data_hour[i].cur_weather
            weather_photo = self.weather_photo[weather]
            self.canvas.create_text(40+80*i, 200, text=time, font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            self.show_picture(weather_photo, 30, 30, 40+80*i-15, 220)
            self.canvas.create_text(40+80*i, 280, text=str(temp)+"°", font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
        
        # 提醒功能
        reminder = Reminder()
        for i in range(24):
            reminder.set_reminder_by_weather(city.weather_forecast.weather_data_hour[i])
            if reminder.message:
                self.show_picture("pic/white_rec.png", 390, 100, 5, 520)
                self.canvas.create_text(200, 550, text=reminder.message, font=("微软雅黑", 14,"bold"), fill="black")
                break
        
        #设置
        self.canvas.create_text(30, 20, text="设置", font=("微软雅黑", 12,"bold"), fill="white")
        #切换城市
        self.canvas.create_text(350, 20, text = "切换城市", font=("微软雅黑", 12,"bold"), fill="white")
        self.change_city_trigger_area = {
            'x1': 320,
            'y1': 10,
            'x2': 380,
            'y2': 30
        }
        
        #查看今天的具体天气预报
        self.hour_forecast_trigger_area = {
            'x1': 20,
            'y1': 200,
            'x2': 380,
            'y2': 280,   
        }
        #查看未来一周的天气预报
        self.day_forecast_trigger_area = {
            'x1': 20,
            'y1': 350,
            'x2': 380,
            'y2': 510,
        }
        #设置按钮
        self.setting_trigger_area = {
            'x1': 20,
            'y1': 10,
            'x2': 80,
            'y2': 30
        }
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):

        x, y = event.x, event.y
        if self.cur_screen == "MainScreen":
            #切换城市
            if self.change_city_trigger_area['x1'] <= x <= self.change_city_trigger_area['x2'] and self.change_city_trigger_area['y1'] <= y <= self.change_city_trigger_area['y2']:
                self.show_cities()
            
            #查看今天的具体天气预报
            elif self.hour_forecast_trigger_area['x1'] <= x <= self.hour_forecast_trigger_area['x2'] and self.hour_forecast_trigger_area['y1'] <= y <= self.hour_forecast_trigger_area['y2']:
                self.show_hour_forecast()
            
            #查看未来一周的天气预报
            elif self.day_forecast_trigger_area['x1'] <= x <= self.day_forecast_trigger_area['x2'] and self.day_forecast_trigger_area['y1'] <= y <= self.day_forecast_trigger_area['y2']:
                self.show_day_forecast()
            elif self.setting_trigger_area['x1'] <= x <= self.setting_trigger_area['x2'] and self.setting_trigger_area['y1'] <= y <= self.setting_trigger_area['y2']:
                self.show_setting()
            else:
                return
        elif self.cur_screen == "Setting":
            if self.setting_trigger_area['x1'] <= x <= self.setting_trigger_area['x2'] and self.setting_trigger_area['y1'] <= y <= self.setting_trigger_area['y2']:
                if self.is_on.get():
                    #self.canvas.itemconfig(self.bg, fill="white")
                    self.canvas.itemconfig(self.oval, fill="grey")
                    self.is_on.set(False)
                else:
                    #self.canvas.itemconfig(self.bg, fill="grey")
                    self.canvas.itemconfig(self.oval, fill="green")
                    self.is_on.set(True)
            self.current_user.settings.night_mode = self.is_on.get()
            self.show_setting()    
    
    def login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        
        is_valid = False
        for user in self.db.users:
            if user.id == user_id and user.password == password:
                is_valid = True
                self.current_user = user
                break
        
        if is_valid:
            self.show_main_screen()
        else:
            messagebox.showerror("错误", "用户名或密码错误")
    
    def register(self):
        user_id = self.new_user_id_entry.get()
        password = self.new_password_entry.get()
        
        # 检查用户是否已存在
        for user in self.db.users:
            if user.id == user_id:
                messagebox.showerror("错误", "用户ID已存在")
                return
        
        # 创建新用户
        theme = self.db.themes[0]  # 使用第一个主题
        location = Location('南京', 32.04, 118.78)
        new_user = User(user_id, password, Settings(False, theme), location, [])
        self.db.users.append(new_user)
        messagebox.showinfo("成功", "注册成功")
        self.show_login()

    def change_to_city(self, city_name):
        city = Location(city_name, 0, 0)
        self.current_user.current_location = city
        self.show_main_screen()

    def show_search_city(self):
        
        name=self.search_city_entry.get()

        self.cur_screen = "Search_Cities"
        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)

        self.canvas.create_text(50, 80, text=" 切换城市", font=("微软雅黑", 14, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(320,80, text="当前城市："+ self.current_user.current_location.city_name, font=("微软雅黑", 14,"bold"), fill=self.word_color[self.current_user.settings.night_mode])
        

        city_name = name
        
        find = False
        if city_name in self.city_list:
            find = True
        
        if find:
            self.canvas.create_text(50, 150, text="搜索结果：", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
            self.canvas.create_text(50, 180, text=city_name, font=("微软雅黑", 14, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
            add_button = tk.Button(self.window, text="加入收藏", command=lambda: self.add_cities(city_name))
            change_button = tk.Button(self.window, text="切换", command=lambda: self.change_to_city(city_name))
            self.canvas.create_window(300, 180, window=add_button, width=50, height=30)
            self.canvas.create_window(360, 180, window=change_button, width=50, height=30)
        else:
            messagebox.showwarning("搜索失败", "未找到该城市，请重新输入。")
            self.show_cities()

    def add_cities(self,city_name):
        city = Location(city_name, 0, 0)
        self.current_user.favorite_locations.append(city)
        messagebox.showwarning("添加成功", "已将"+city_name+"添加到收藏。")
        self.show_cities()

    def show_cities(self):
        self.cur_screen = "Cities"

        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)
        self.canvas.create_text(50, 80, text=" 切换城市", font=("微软雅黑", 14, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(320,80, text="当前城市："+ self.current_user.current_location.city_name, font=("微软雅黑", 14,"bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        self.search_city_entry = tk.Entry(self.window)
        self.canvas.create_window(170, 110, window=self.search_city_entry, width=320)
        self.search_button = tk.Button(self.window, text="搜索", bg ="white", command = self.show_search_city)
        self.canvas.create_window(360, 112, window=self.search_button, width=60, height=24)

        self.canvas.create_text(50, 150, text="你的收藏：", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        for i in range(len(self.current_user.favorite_locations)):
            self.canvas.create_text(50, 180+30*i, text=self.current_user.favorite_locations[i].city_name, font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
            change_button = tk.Button(self.window, text="切换", command=lambda i=i: self.change_city(i))
            self.canvas.create_window(350, 180+30*i, window=change_button, width=50, height=20)

        #返回按钮
        self.back_button = tk.Button(self.window, text="返回", command=self.show_main_screen)
        self.canvas.create_window(350, 450, window=self.back_button, width=100, height=30)
    
    def change_city(self, index):
        self.current_user.current_location = self.current_user.favorite_locations[index]
        self.show_main_screen()

    def show_hour_forecast(self):
        self.cur_screen = "HourForecast"

        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)
        self.show_picture("pic/rectangle.png", 390, 100, 5, 98)
        self.canvas.create_text(60, 80, text="今日天气", font=("微软雅黑", 16, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        city = self.current_user.current_location
        for i in range(5):
            if i == 0 :
                time = "现在"
            else :
                time = city.weather_forecast.weather_data_hour[i].timestamp.strftime("%H:%M")

            temp = city.weather_forecast.weather_data_hour[i].cur_temperature
            weather = city.weather_forecast.weather_data_hour[i].cur_weather
            weather_photo = self.weather_photo[weather]
            self.canvas.create_text(40+80*i, 120, text=time, font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            self.show_picture(weather_photo, 30, 30, 40+80*i-15, 140)
            self.canvas.create_text(40+80*i, 180, text=str(temp)+"°", font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
        
        #细节天气
        #AQI
        self.show_picture("pic/rec_aqi.png", 200, 80, 5, 210)
        self.show_picture("pic/aqi.png", 30, 30, 20, 220)
        self.canvas.create_text(85, 235, text="  ：AQI", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        aqi = city.weather_forecast.weather_data_hour[0].pollution_level
        self.canvas.create_text(90, 260, text="当前空气质量指数：" + 
                                str(aqi), font=("微软雅黑", 10, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        #风力和风速
        self.show_picture("pic/rec_wind.png", 160, 80, 230, 210)
        wind_direaction = city.weather_forecast.weather_data_hour[0].wind_direction
        wind_speed = city.weather_forecast.weather_data_hour[0].wind_speed
        self.show_picture("pic/direction.png", 30, 30, 250, 220)
        self.canvas.create_text(305, 235, text=" ："+wind_direaction, font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        wind_level = city.weather_forecast.judge_windSPeed(wind_speed)
        self.canvas.create_text(305, 260, text = wind_level + "  "+wind_speed, font=("微软雅黑", 10, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        

        #能见度
        self.show_picture("pic/rec_wind.png", 170, 80, 5, 305)
        visibility = city.weather_forecast.weather_data_hour[0].visibility
        vis_level = city.weather_forecast.judge_visibility(visibility)
        self.canvas.create_text(45, 325, text="能见度:", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(65, 355, text=str(visibility)+"公里", font=("微软雅黑", 20, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(150, 345, text="视野", font=("微软雅黑", 10, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(150, 365, text=vis_level, font=("微软雅黑", 10, "bold"), fill=self.word_color[self.current_user.settings.night_mode])


        #湿度
        self.show_picture("pic/rec_wind.png", 210, 80, 180, 305)
        humidity = city.weather_forecast.weather_data_hour[0].humidity
        self.canvas.create_text(235, 325, text="湿度:", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(290, 355, text=str(humidity)+"%", font=("微软雅黑", 20, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        
        #降雨概率
        self.show_picture("pic/rec_wind.png", 260, 80, 5, 390)
        rain = city.weather_forecast.weather_data_hour[0].probability_of_rain
        self.canvas.create_text(50, 415, text="降雨概率:", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(100, 445, text=str(rain)+"%", font=("微软雅黑", 20, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.show_picture("pic/rain.png", 50, 50, 150, 410)

        #返回
        self.back_button = tk.Button(self.window, text="返回", command=self.show_main_screen)
        self.canvas.create_window(350, 450, window=self.back_button, width=100, height=30)

    def show_day_forecast(self):
        self.cur_screen = "DayForecast"

        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)
        self.show_picture("pic/rec_dayforecast.png", 380, 490, 10, 65)
        self.canvas.create_text(100, 50, text="两周内天气预报", font=("微软雅黑", 14, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        
        city = self.current_user.current_location
        week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i in range(12):
            if i == 0:
                date = "今天"
            else:
                date = week_list[city.weather_forecast.weather_data_day[i].timestamp.weekday()]
            
            high_temp = city.weather_forecast.weather_data_day[i].high_temperature
            low_temp = city.weather_forecast.weather_data_day[i].low_temperature
            cur_weather = city.weather_forecast.weather_data_day[i].cur_weather

            self.canvas.create_text(50, 90+40*i, text=date, font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            weather_photo = self.weather_photo[cur_weather]
            self.show_picture(weather_photo, 30, 30, 100, 75+40*i)
            self.canvas.create_text(280, 90+40*i, text=str(low_temp)+"°"+"————"+
                                    str(high_temp)+"°", font=("微软雅黑", 12), fill=self.word_color[self.current_user.settings.night_mode])
            if (i != 0):
                self.show_picture("pic/line.png", 370, 2, 15, 70+40*i)
        self.back_button = tk.Button(self.window, text="返回", command=self.show_main_screen)
        self.canvas.create_window(350, 50, window=self.back_button, width=100, height=30)

    def show_setting(self):
        self.cur_screen = "Setting"

        self.canvas.delete("all")
        self.show_picture(self.bg_color[self.current_user.settings.night_mode], 400, 600, 0, 0)
        self.canvas.create_text(50, 80, text="设置", font=("微软雅黑", 20, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.show_picture("pic/line_white.png", 380, 2, 10, 105)
        self.canvas.create_text(65, 130, text="夜间模式", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.show_picture("pic/line_white.png", 380, 2, 10, 150)

        self.is_on = tk.BooleanVar(value=self.current_user.settings.night_mode) # 夜间模式开关状态
        self.bg = self.canvas.create_oval(330, 120, 350, 140, fill="white", outline="")
        if self.current_user.settings.night_mode:
            self.oval = self.canvas.create_oval(332, 122, 348, 138, fill="green", outline="")
        else:
            self.oval = self.canvas.create_oval(332, 122, 348, 138, fill="grey", outline="")
        self.setting_trigger_area = {
            'x1': 330,
            'y1': 120,
            'x2': 350,
            'y2': 140
        }
        if self.current_user.settings.night_mode:
            self.canvas.create_text(360, 130, text="开", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        else:
            self.canvas.create_text(360, 130, text="关", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])

        #主题
        self.canvas.create_text(48, 170, text="主题", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        self.canvas.create_text(350, 170, text="默认", font=("微软雅黑", 12, "bold"), fill=self.word_color[self.current_user.settings.night_mode])
        

        #返回
        self.back_button = tk.Button(self.window, text="返回", command=self.show_main_screen)
        self.canvas.create_window(350, 80, window=self.back_button, width=100, height=30)

def main():
    window = tk.Tk()
    MainScreen(window)
    window.mainloop()

if __name__ == '__main__':
    main()