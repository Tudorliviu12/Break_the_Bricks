from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Brick(QGraphicsPixmapItem):
    def __init__(self, color):
        super().__init__()
        pixmap = QPixmap(f"assets/images/{color}.png")
        pixmap = pixmap.scaled(60,25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)