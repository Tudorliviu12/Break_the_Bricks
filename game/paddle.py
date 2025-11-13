from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Paddle(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        paddle_pixmap = QPixmap('assets/images/paddle.png')
        paddle_pixmap = paddle_pixmap.scaled(100,20,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(paddle_pixmap)
        self.setPos(300,450)