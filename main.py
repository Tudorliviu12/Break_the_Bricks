import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_menu import MainMenu

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/images/ball.png'))

    main_menu = MainMenu()
    main_menu.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()