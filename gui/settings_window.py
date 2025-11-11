from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from .styles import BUTTON_STYLE


class SettingsWidget(QWidget):
    settings_changed = pyqtSignal(dict)
    back_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.colored_bricks = True
        self.sound_enabled = True

        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        background = QPixmap('assets/images/fundal.jpg').scaled(700, 500, Qt.KeepAspectRatioByExpanding,
                                                               Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(15)

        title_label = QLabel("SETTINGS")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #bbe1fa;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Impact', 'Arial Black', sans-serif;
                background: transparent;
                padding: 10px;
                letter-spacing: 3px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            }
        """)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(15)

        color_group = QGroupBox("Brick Colors")
        color_group.setStyleSheet("""
            QGroupBox {
                color: #bbe1fa;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial;
                border: 3px solid #3bb4c1;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px 20px 15px 20px;
                background: rgba(11, 35, 50, 0.95);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 15px;
                background: #0f4c75;
                border-radius: 5px;
            }
        """)

        color_layout = QHBoxLayout()
        color_layout.setSpacing(15)
        color_layout.setContentsMargins(10, 10, 10, 10)

        self.colored_button = QPushButton("Colored")
        self.colored_button.setCheckable(True)
        self.colored_button.setChecked(True)
        self.colored_button.setStyleSheet(self.get_color_button_style())
        self.colored_button.clicked.connect(self.on_colored_clicked)

        self.grayscale_button = QPushButton("Grayscale")
        self.grayscale_button.setCheckable(True)
        self.grayscale_button.setChecked(False)
        self.grayscale_button.setStyleSheet(self.get_color_button_style())
        self.grayscale_button.clicked.connect(self.on_grayscale_clicked)

        color_layout.addWidget(self.colored_button)
        color_layout.addWidget(self.grayscale_button)
        color_group.setLayout(color_layout)

        main_layout.addWidget(color_group)
        main_layout.addSpacing(20)

        sound_group = QGroupBox("Sound Effects")
        sound_group.setStyleSheet("""
            QGroupBox {
                color: #bbe1fa;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial;
                border: 3px solid #3bb4c1;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px 20px 15px 20px;
                background: rgba(11, 35, 50, 0.95);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 15px;
                background: #0f4c75;
                border-radius: 5px;
            }
        """)

        sound_layout = QHBoxLayout()
        sound_layout.setSpacing(15)
        sound_layout.setContentsMargins(10, 10, 10, 10)

        sound_layout.addStretch()

        self.sound_button = QPushButton("ON")
        self.sound_button.setCheckable(True)
        self.sound_button.setChecked(True)
        self.sound_button.setStyleSheet(self.get_sound_button_style())
        self.sound_button.clicked.connect(self.on_sound_clicked)

        sound_layout.addWidget(self.sound_button)
        sound_layout.addStretch()
        sound_group.setLayout(sound_layout)

        main_layout.addWidget(sound_group)

        main_layout.addStretch(1)

        back_button = QPushButton("BACK TO MENU")
        back_button.setStyleSheet(BUTTON_STYLE)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.back_to_menu)

        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def get_color_button_style(self):
        return """
            QPushButton {
                background: #1b262c;
                border: 2px solid #3bb4c1;
                border-radius: 8px;
                color: #bbe1fa;
                font-size: 15px;
                font-weight: bold;
                font-family: Arial;
                padding: 12px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                border: 2px solid #5dd4e5;
                background: #0f4c75;
            }
            QPushButton:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3bb4c1,
                    stop:1 #1764a0
                );
                border: 2px solid #5dd4e5;
                color: #ffffff;
            }
            QPushButton:checked:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dd4e5,
                    stop:1 #3bb4c1
                );
            }
        """

    def get_sound_button_style(self):
        return """
            QPushButton {
                background: #1b262c;
                border: 2px solid #3bb4c1;
                border-radius: 8px;
                color: #bbe1fa;
                font-size: 15px;
                font-weight: bold;
                font-family: Arial;
                padding: 12px 30px;
                min-width: 100px;
            }
            QPushButton:hover {
                border: 2px solid #5dd4e5;
                background: #0f4c75;
            }
            QPushButton:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ecdc4,
                    stop:1 #2a9d8f
                );
                border: 2px solid #5dd4e5;
                color: #ffffff;
            }
            QPushButton:checked:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dd4e5,
                    stop:1 #4ecdc4
                );
            }
        """

    def on_colored_clicked(self):
        self.colored_button.setChecked(True)
        self.grayscale_button.setChecked(False)
        self.colored_bricks = True

    def on_grayscale_clicked(self):
        self.grayscale_button.setChecked(True)
        self.colored_button.setChecked(False)
        self.colored_bricks = False

    def on_sound_clicked(self, checked):
        self.sound_enabled = checked
        if checked:
            self.sound_button.setText("ON")
        else:
            self.sound_button.setText("OFF")

    def back_to_menu(self):
        settings = {
            'colored_bricks': self.colored_bricks,
            'sound_enabled': self.sound_enabled
        }
        self.settings_changed.emit(settings)
        self.back_button_clicked.emit()