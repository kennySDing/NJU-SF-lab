from .theme import Theme

class Settings:
    def __init__(self, night_mode: bool, theme: Theme):
        self.night_mode = night_mode
        self.theme = theme
