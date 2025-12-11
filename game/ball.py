from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Ball(QGraphicsPixmapItem):
    def __init__(self, is_grayscale=False):
        super().__init__()
        if is_grayscale:
            image_name = 'assets/images/ball2.png'
        else:
            image_name = 'assets/images/ball.png'

        ball_pixmap = QPixmap(image_name)
        ball_pixmap = ball_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(ball_pixmap)

        self.setPos(340, 240)

        self.dx = 3
        self.dy = 3