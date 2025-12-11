from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Brick(QGraphicsPixmapItem):
    def __init__(self, color, is_grayscale=False):
        super().__init__()
        self.brick_color = color
        self.is_grayscale = is_grayscale
        self.health = 2

        self.update_image()

    def update_image(self):
        if self.is_grayscale:
            if self.health == 2:
                image_name = "assets/images/gray.png"
            else:
                image_name = "assets/images/gray2.png"
        else:
            if self.health == 2:
                image_name = f"assets/images/{self.brick_color}.png"
            else:
                image_name = f"assets/images/{self.brick_color}2.png"

        pixmap = QPixmap(image_name)
        pixmap = pixmap.scaled(60,25,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def hit(self):
        self.health = self.health - 1
        if self.health > 0:
            self.update_image()
            return False
        else:
            return True