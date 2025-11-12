from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap


class GameWindow(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.lives = 3
        self.score = 0
        self.game_started = False

        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        background = QPixmap('assets/images/fundal.jpg').scaled(700, 500, Qt.KeepAspectRatioByExpanding,
                                                               Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 500)

        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFixedSize(700, 500)
        self.view.setStyleSheet("border: none; background: transparent;")

        layout.addWidget(self.view)
        self.setLayout(layout)

        self.countdown_label = QLabel(self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 150px;
                font-weight: bold;
                font-family: 'Impact', 'Arial Black', sans-serif;
                background: transparent;
                text-shadow: 
                    -4px -4px 0 #000,
                    4px -4px 0 #000,
                    -4px 4px 0 #000,
                    4px 4px 0 #000,
                    0 0 20px rgba(0, 0, 0, 0.8);
            }
        """)
        self.countdown_label.setGeometry(0, 0, 700, 500)
        self.countdown_label.hide()

        self.start_countdown()

    def start_countdown(self):
        self.countdown_label.show()
        self.countdown_value = 3
        self.countdown_label.setText(str(self.countdown_value))

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown_value -= 1

        if self.countdown_value > 0:
            self.countdown_label.setText(str(self.countdown_value))
        elif self.countdown_value == 0:
            self.countdown_label.setText("GO!")
        else:
            self.countdown_timer.stop()
            self.countdown_label.hide()
            self.start_game()

    def start_game(self):
        self.game_started = True
        print("Game started!")