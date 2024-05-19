import sys
from gui import MainWindow
from PySide6.QtWidgets import QApplication
from gui.mechanics import Robot

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    