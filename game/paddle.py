from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Paddle(QGraphicsPixmapItem):
    def __init__(self, is_grayscale=False):
        super().__init__()

        image_name = 'assets/images/paddle2.png' if is_grayscale else 'assets/images/paddle.png'
        paddle_pixmap = QPixmap(image_name)
        paddle_pixmap = paddle_pixmap.scaled(100, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(paddle_pixmap)
        self.setPos(300, 450)