from src import RobotGUI
from PySide6.QtWidgets import QApplication


# from src import Robot
# robot = Robot()
# robot.set_end_point([-14.04, 72.67])

app = QApplication([])
robot_bui = RobotGUI()
app.exec()