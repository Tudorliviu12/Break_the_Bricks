from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, \
    QGraphicsPixmapItem
from gui.styles import BUTTON_STYLE
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap


class GameWindow(QWidget):
    def __init__(self, settings, sound_manager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.lives = 3
        self.score = 0
        self.sound_manager = sound_manager
        self.game_started = False
        self.ball_frozen = False
        self.heart_items = []
        self.keys_pressed = set()
        self.is_grayscale = not self.settings.get('colored_bricks', True)
        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        bg_image = 'assets/images/fundal2.png' if self.is_grayscale else 'assets/images/fundal.jpg'
        background = QPixmap(bg_image).scaled(700, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
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
        self.setFocusPolicy(Qt.StrongFocus)

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

        self.end_message_label = QLabel(self)
        self.end_message_label.setAlignment(Qt.AlignCenter)
        self.end_message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 72px;
                font-weight: bold;
                font-family: 'Impact', 'Arial Black', sans-serif;
                background: rgba(0, 0, 0, 150);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        self.end_message_label.setGeometry(0, 0, 700, 500)
        self.end_message_label.hide()

        self.end_buttons_container = QWidget(self)
        self.end_buttons_container.setGeometry(0, 0, 700, 800)
        self.end_buttons_container.hide()

        buttons_layout = QVBoxLayout(self.end_buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 50)
        buttons_layout.setSpacing(15)

        buttons_layout.addStretch(1)

        row = QHBoxLayout()
        row.addStretch(1)

        self.play_again_button = QPushButton("PLAY AGAIN")
        self.play_again_button.setStyleSheet(BUTTON_STYLE)
        self.play_again_button.setCursor(Qt.PointingHandCursor)
        self.play_again_button.clicked.connect(self.restart_game)
        row.addWidget(self.play_again_button)

        row.addSpacing(20)

        self.exit_button = QPushButton("EXIT TO MENU")
        self.exit_button.setStyleSheet(BUTTON_STYLE)
        self.exit_button.setCursor(Qt.PointingHandCursor)
        self.exit_button.clicked.connect(self.exit_to_menu)
        row.addWidget(self.exit_button)

        row.addStretch(1)

        buttons_layout.addLayout(row)
        buttons_layout.addStretch(1)

        self.setup_game_elements()
        self.start_countdown()

    def setup_game_elements(self):
        from game.paddle import Paddle
        from game.ball import Ball

        self.paddle = Paddle(is_grayscale=self.is_grayscale)
        self.scene.addItem(self.paddle)

        self.ball = Ball(is_grayscale=self.is_grayscale)
        self.scene.addItem(self.ball)

        self.movement_timer = QTimer()
        self.movement_timer.timeout.connect(self.update_movement)
        self.movement_timer.start(16)

        self.create_bricks()
        self.draw_hearts()

    def create_bricks(self):
        from game.brick import Brick

        self.bricks = []
        colors = ["red", "yellow", "green", "blue"]
        rows = 4
        cols = 10

        start_x = 20
        start_y = 30
        spacing_x = 65
        spacing_y = 35

        for row in range(rows):
            for col in range(cols):
                color = colors[row]
                brick = Brick(color, is_grayscale=self.is_grayscale)
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                brick.setPos(x, y)
                self.scene.addItem(brick)
                self.bricks.append(brick)

    def draw_hearts(self):
        for heart in self.heart_items:
            self.scene.removeItem(heart)
        self.heart_items.clear()

        heart_img = 'assets/images/heart2.png' if self.is_grayscale else 'assets/images/heart.png'

        heart_pixmap = QPixmap(heart_img)
        heart_pixmap = heart_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        for i in range(self.lives):
            heart_item = QGraphicsPixmapItem(heart_pixmap)
            heart_item.setPos(660 - (i * 35), 10)
            self.scene.addItem(heart_item)
            self.heart_items.append(heart_item)

    def reset_ball_and_paddle(self):
        self.ball.setPos(340, 240)
        self.ball.dx = 3
        self.ball.dy = 3
        self.ball.dy = -abs(self.ball.dy)
        self.paddle.setPos(300, 450)

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

    def show_end_message(self, text):
        self.end_message_label.setText(text)
        self.end_message_label.show()
        self.end_buttons_container.show()
        self.game_started = False

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.discard(event.key())

    def update_movement(self):
        if not self.game_started or not hasattr(self, 'paddle'):
            return

        paddle_speed = 5

        if Qt.Key_Left in self.keys_pressed or Qt.Key_A in self.keys_pressed:
            new_x = self.paddle.x() - paddle_speed
            if new_x >= 0:
                self.paddle.setX(new_x)

        if Qt.Key_Right in self.keys_pressed or Qt.Key_D in self.keys_pressed:
            new_x = self.paddle.x() + paddle_speed
            if new_x + self.paddle.pixmap().width() <= 700:
                self.paddle.setX(new_x)

        if self.ball_frozen:
            return

        self.ball.setPos(self.ball.x() + self.ball.dx, self.ball.y() + self.ball.dy)

        if self.ball.x() <= 0 or self.ball.x() + self.ball.pixmap().width() >= 700:
            self.ball.dx = -self.ball.dx
            #self.sound_manager.play_hit_sound()

        if self.ball.y() <= 0:
            self.ball.dy = -self.ball.dy
            #self.sound_manager.play_hit_sound()

        if self.ball.y() + self.ball.pixmap().height() >= 500:
            self.lives -= 1

            if self.heart_items:
                last_heart = self.heart_items.pop()
                self.scene.removeItem(last_heart)

            if self.lives <= 0:
                self.end_game(won=False)
                return
            else:
                self.reset_ball_and_paddle()
                self.ball_frozen = True
                QTimer.singleShot(1000, self.unfreeze_ball)
                return

        if self.ball.collidesWithItem(self.paddle):
            self.ball.dy = -abs(self.ball.dy)
            self.ball.setY(self.paddle.y() - self.ball.pixmap().height())

            #self.sound_manager.play_hit_sound()

            paddle_center = self.paddle.x() + self.paddle.pixmap().width() / 2
            ball_center = self.ball.x() + self.ball.pixmap().width() / 2
            offset = (paddle_center - ball_center) / 50
            self.ball.dx = self.ball.dx + offset

        colliding_items = self.ball.collidingItems()
        for item in colliding_items:
            if item in self.bricks:
                self.ball.dy = -self.ball.dy
                #self.sound_manager.play_hit_sound()
                is_destroyed = item.hit()
                if is_destroyed:
                    self.scene.removeItem(item)
                    self.bricks.remove(item)
                    self.score += 10
                    if len(self.bricks) == 0:
                        self.end_game(won=True)
                break

    def unfreeze_ball(self):
        if self.game_started:
            self.ball_frozen = False

    def end_game(self, won: bool):
        self.game_started = False
        if hasattr(self, "movement_timer"):
            self.movement_timer.stop()

        if won:
            text = f"You won!\nScore: {self.score}"
        else:
            text = f"Game Over!\nScore: {self.score}"

        self.show_end_message(text)

    def restart_game(self):
        self.end_message_label.hide()
        self.end_buttons_container.hide()
        self.ball_frozen = False
        self.lives = 3
        self.score = 0

        if hasattr(self, "bricks"):
            for brick in self.bricks:
                self.scene.removeItem(brick)
        self.bricks = []

        self.create_bricks()

        self.reset_ball_and_paddle()
        self.draw_hearts()

        if hasattr(self, "movement_timer"):
            self.movement_timer.start(16)

        self.start_countdown()

    def exit_to_menu(self):
        self.game_started = False
        if hasattr(self, "movement_timer"):
            self.movement_timer.stop()

        self.end_message_label.hide()
        self.end_buttons_container.hide()

        parent = self.parent()
        while parent is not None and not hasattr(parent, "show_menu"):
            parent = parent.parent()

        if parent is not None and hasattr(parent, "show_menu"):
            parent.show_menu()