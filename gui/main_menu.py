from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QApplication, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .styles import BUTTON_STYLE, BACKGROUND_STYLE, BUTTON_STYLE_GRAY
from .settings_window import SettingsWidget


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Break the Bricks!")
        self.setFixedSize(700, 500)
        self.game_settings = {
            'colored_bricks': True,
            'sound_enabled': True
        }
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.menu_page = self.create_menu_page()
        self.settings_page = SettingsWidget(self)
        self.settings_page.back_button_clicked.connect(self.show_menu)
        self.settings_page.settings_changed.connect(self.update_settings)

        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.setCentralWidget(self.stacked_widget)

        self.update_menu_appearance()

    def create_menu_page(self):
        self.menu_container = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.title_label)
        layout.addStretch(1)

        self.start_button = QPushButton("START GAME")
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_game)

        self.settings_button = QPushButton("SETTINGS")
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.clicked.connect(self.show_settings)

        self.exit_button = QPushButton("EXIT")
        self.exit_button.setCursor(Qt.PointingHandCursor)
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.start_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.exit_button)
        layout.addStretch(1)
        self.menu_container.setLayout(layout)

        return self.menu_container

    def show_settings(self):
        self.settings_page.colored_button.setChecked(self.game_settings['colored_bricks'])
        self.settings_page.grayscale_button.setChecked(not self.game_settings['colored_bricks'])
        self.settings_page.sound_button.setChecked(self.game_settings['sound_enabled'])
        self.settings_page.sound_button.setText("ON" if self.game_settings['sound_enabled'] else "OFF")

        is_grayscale = not self.game_settings['colored_bricks']
        self.settings_page.update_appearance(is_grayscale)

        self.stacked_widget.setCurrentWidget(self.settings_page)

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def update_settings(self, settings):
        self.game_settings = settings
        self.update_menu_appearance()

    def update_menu_appearance(self):
        is_grayscale = not self.game_settings.get('colored_bricks', True)
        title_img = 'assets/images/title2.png' if is_grayscale else 'assets/images/title.png'
        pixmap = QPixmap(title_img)
        pixmap = pixmap.scaledToWidth(380, Qt.SmoothTransformation)
        self.title_label.setPixmap(pixmap)

        bg_img = 'assets/images/fundal2.png' if is_grayscale else 'assets/images/fundal.jpg'
        new_bg_style = f"""
            QWidget {{
                background-image: url('{bg_img}');
                background-repeat: no-repeat;
                background-position: center;
            }}
        """
        self.menu_container.setStyleSheet(new_bg_style)
        current_style = BUTTON_STYLE_GRAY if is_grayscale else BUTTON_STYLE

        self.start_button.setStyleSheet(current_style)
        self.settings_button.setStyleSheet(current_style)
        self.exit_button.setStyleSheet(current_style)

    def start_game(self):
        from game.game_window import GameWindow
        self.game_window = GameWindow(self.game_settings, parent=self)
        self.stacked_widget.addWidget(self.game_window)
        self.stacked_widget.setCurrentWidget(self.game_window)