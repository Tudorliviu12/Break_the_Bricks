from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from .styles import BUTTON_STYLE, BUTTON_STYLE_GRAY


class SettingsWidget(QWidget):
    settings_changed = pyqtSignal(dict)
    back_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.colored_bricks = True
        self.sound_enabled = True
        self.init_ui()

    def init_ui(self):
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(15)

        self.title_label = QLabel("SETTINGS")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(15)

        self.color_group = QGroupBox("Brick Colors")

        color_layout = QHBoxLayout()
        color_layout.setSpacing(15)
        color_layout.setContentsMargins(10, 10, 10, 10)

        self.colored_button = QPushButton("Colored")
        self.colored_button.setCheckable(True)
        self.colored_button.setChecked(True)
        self.colored_button.clicked.connect(self.on_colored_clicked)

        self.grayscale_button = QPushButton("Grayscale")
        self.grayscale_button.setCheckable(True)
        self.grayscale_button.setChecked(False)
        self.grayscale_button.clicked.connect(self.on_grayscale_clicked)

        color_layout.addWidget(self.colored_button)
        color_layout.addWidget(self.grayscale_button)
        self.color_group.setLayout(color_layout)
        main_layout.addWidget(self.color_group)
        main_layout.addSpacing(20)

        self.sound_group = QGroupBox("Sound Effects")

        sound_layout = QHBoxLayout()
        sound_layout.setSpacing(15)
        sound_layout.setContentsMargins(10, 10, 10, 10)
        sound_layout.addStretch()

        self.sound_button = QPushButton("ON")
        self.sound_button.setCheckable(True)
        self.sound_button.setChecked(True)
        self.sound_button.clicked.connect(self.on_sound_clicked)

        sound_layout.addWidget(self.sound_button)
        sound_layout.addStretch()
        self.sound_group.setLayout(sound_layout)
        main_layout.addWidget(self.sound_group)
        main_layout.addStretch(1)

        self.back_button = QPushButton("BACK TO MENU")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_to_menu)
        main_layout.addWidget(self.back_button)

        self.setLayout(main_layout)

        self.update_appearance(not self.colored_bricks)

    def update_appearance(self, is_grayscale):
        palette = QPalette()
        img_name = 'assets/images/fundal2.png' if is_grayscale else 'assets/images/fundal.jpg'
        background = QPixmap(img_name).scaled(700, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        border_color = "#808080" if is_grayscale else "#3bb4c1"
        bg_color = "rgba(40, 40, 40, 0.95)" if is_grayscale else "rgba(11, 35, 50, 0.95)"
        text_color = "#d9d9d9" if is_grayscale else "#bbe1fa"
        header_bg = "#404040" if is_grayscale else "#0f4c75"

        group_style = f"""
            QGroupBox {{
                color: {text_color};
                font-size: 18px;
                font-weight: bold;
                font-family: Arial;
                border: 3px solid {border_color};
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px 20px 15px 20px;
                background: {bg_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 15px;
                background: {header_bg};
                border-radius: 5px;
            }}
        """
        self.color_group.setStyleSheet(group_style)
        self.sound_group.setStyleSheet(group_style)

        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 36px;
                font-weight: bold;
                font-family: 'Impact', 'Arial Black', sans-serif;
                background: transparent;
                padding: 10px;
                letter-spacing: 3px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            }}
        """)

        self.back_button.setStyleSheet(BUTTON_STYLE_GRAY if is_grayscale else BUTTON_STYLE)

        self.colored_button.setStyleSheet(self.get_toggle_style(is_grayscale))
        self.grayscale_button.setStyleSheet(self.get_toggle_style(is_grayscale))
        self.sound_button.setStyleSheet(self.get_toggle_style(is_grayscale))

    def get_toggle_style(self, is_grayscale):
        base_color = "#404040" if is_grayscale else "#1b262c"
        border = "#808080" if is_grayscale else "#3bb4c1"
        text = "#d9d9d9" if is_grayscale else "#bbe1fa"

        checked_start = "#808080" if is_grayscale else "#3bb4c1"
        checked_end = "#404040" if is_grayscale else "#1764a0"

        return f"""
            QPushButton {{
                background: {base_color};
                border: 2px solid {border};
                border-radius: 8px;
                color: {text};
                font-size: 15px;
                font-weight: bold;
                font-family: Arial;
                padding: 12px 20px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                border: 2px solid #ffffff;
            }}
            QPushButton:checked {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {checked_start},
                    stop:1 {checked_end}
                );
                color: #ffffff;
                border: 2px solid #ffffff;
            }}
        """

    def on_colored_clicked(self):
        self.colored_button.setChecked(True)
        self.grayscale_button.setChecked(False)
        self.colored_bricks = True
        self.update_appearance(False)

    def on_grayscale_clicked(self):
        self.grayscale_button.setChecked(True)
        self.colored_button.setChecked(False)
        self.colored_bricks = False
        self.update_appearance(True)

    def on_sound_clicked(self, checked):
        self.sound_enabled = checked
        self.sound_button.setText("ON" if checked else "OFF")

    def back_to_menu(self):
        settings = {
            'colored_bricks': self.colored_bricks,
            'sound_enabled': self.sound_enabled
        }
        self.settings_changed.emit(settings)
        self.back_button_clicked.emit()