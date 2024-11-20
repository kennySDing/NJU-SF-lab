# theme.py

class Theme:
    def __init__(self, color: str, image: str, size: int):
        self.color = color
        self.image = image
        self.size = size

    def change_color(self, new_color: str):
        self.color = new_color

    def change_image(self, new_image: str):
        self.image = new_image

    def change_size(self, new_size: int):
        self.size = new_size
