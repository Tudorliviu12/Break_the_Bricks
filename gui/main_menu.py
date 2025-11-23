from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QApplication, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .styles import BUTTON_STYLE, BACKGROUND_STYLE
from .settings_window import SettingsWidget

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Break the Bricks!")
        self.setFixedSize(700,500)
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

    def create_menu_page(self):
        container = QWidget()
        container.setStyleSheet(BACKGROUND_STYLE)
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        title = QLabel()
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background: transparent;")
        title_pixmap = QPixmap('assets/images/title.png')
        title_pixmap = title_pixmap.scaledToWidth(380, Qt.SmoothTransformation)
        title.setPixmap(title_pixmap)
        layout.addWidget(title)
        layout.addStretch(1)

        start_button = QPushButton("START GAME")
        start_button.setStyleSheet(BUTTON_STYLE)
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.clicked.connect(self.start_game)

        settings_button = QPushButton("SETTINGS")
        settings_button.setStyleSheet(BUTTON_STYLE)
        settings_button.setCursor(Qt.PointingHandCursor)
        settings_button.clicked.connect(self.show_settings)

        exit_button = QPushButton("EXIT")
        exit_button.setStyleSheet(BUTTON_STYLE)
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.clicked.connect(self.close)

        layout.addWidget(start_button)
        layout.addWidget(settings_button)
        layout.addWidget(exit_button)
        layout.addStretch(1)
        container.setLayout(layout)

        return container

    def show_settings(self):
        self.settings_page.colored_button.setChecked(self.game_settings['colored_bricks'])
        self.settings_page.grayscale_button.setChecked(not self.game_settings['colored_bricks'])
        self.settings_page.sound_button.setChecked(self.game_settings['sound_enabled'])
        self.settings_page.sound_button.setText("ON" if self.game_settings['sound_enabled'] else "OFF")
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def update_settings(self, settings):
        self.game_settings = settings

    def start_game(self):
        from game.game_window import GameWindow
        self.game_window = GameWindow(self.game_settings, parent=self)
        self.stacked_widget.addWidget(self.game_window)
        self.stacked_widget.setCurrentWidget(self.game_window)
