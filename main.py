from src import RobotGUI
from PySide6.QtWidgets import QApplication


from src import Robot
robot = Robot()
robot.set_motor_angles(3.14/2, 3.14/2)
print(robot.get_end_point())

app = QApplication([])
robot_bui = RobotGUI()
app.exec()