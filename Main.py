from PyQt6.QtWidgets import QApplication

from windows.LoginWindow import LoginWindow

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()