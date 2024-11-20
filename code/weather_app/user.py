from typing import List
from .location import Location
from .settings import Settings

class User:
    def __init__(self, user_id: str, password: str, settings: Settings,
                 current_location: Location, favorite_locations: List[Location]):
        self.id = user_id
        self.password = password
        self.settings = settings
        self.current_location = current_location
        self.favorite_locations = favorite_locations

    def register(self):
        # 实现用户注册逻辑
        pass

    def login(self):
        # 实现用户登录逻辑
        pass

    def change_password(self):
        # 实现修改密码逻辑
        pass

    def add_favorite_location(self, location: Location):
        self.favorite_locations.append(location)

    def remove_location(self, location: Location):
        self.favorite_locations.remove(location)

    def update_settings(self, settings: Settings):
        self.settings = settings