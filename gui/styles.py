BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #0f4c75,
            stop:1 #1b262c
        );
        border: 2px solid #3bb4c1;
        border-radius: 10px;
        color: #bbe1fa;
        font-size: 18px;
        font-weight: bold;
        font-family: Arial;
        padding: 8px;
        min-height: 35px;
    }
    QPushButton:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 #1764a0,
            stop:1 #0f4c75
        );
        border: 2px solid #5dd4e5;
    }
    QPushButton:pressed {
        background: #0a3d5c;
        border: 2px solid #2a8ca0;
    }
"""

BACKGROUND_STYLE = """
    QWidget {
        background-image: url('assets/images/fundal.jpg');
        background-repeat: no-repeat;
        background-position: center;
    }
"""