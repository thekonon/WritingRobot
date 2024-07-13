import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.mechanics.robot import Robot

if __name__ == "__main__":
    # app = QApplication()
    # window = MainWindow(app)
    # window.show()
    # sys.exit(app.exec())
    rob = Robot()
    rob.print_current_state()