import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot, Signal
from gui.mechanics.robot import Robot
from gui.graphics import MyGraphicsScene, GridGraphicsView, Drawer
from gui.motor_dial import MotorDial
from math import cos, sin, pi
from typing import List

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.robot: Robot = Robot()

        self.setWindowTitle("RobotController")
        self.setGeometry(100, 100, 600, 600)

        self.canvas_scene: MyGraphicsScene = MyGraphicsScene(self.robot)
        self.canvas_view: GridGraphicsView = GridGraphicsView(self.canvas_scene)
        self.canvas_view.setScene(self.canvas_scene)

        self.connect_button: QPushButton = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button: QPushButton = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)

        self.motor1_dial: MotorDial = MotorDial()
        self.motor1_dial.setMinimum(0)
        self.motor1_dial.setMaximum(360)
        self.motor1_dial.setWrapping(True)
        self.motor1_dial.setNotchesVisible(True)
        self.motor1_dial.setValue(int(self.robot.phi[0] / 3.14 * 180))
        self.motor1_dial.setInvertedAppearance(True)
        self.motor1_dial.dialValueWhileDragging.connect(self.set_motor1_speed)

        self.motor2_dial: MotorDial = MotorDial()
        self.motor2_dial.setMinimum(0)
        self.motor2_dial.setMaximum(360)
        self.motor2_dial.setValue(int(self.robot.phi[1] / 3.14 * 360))
        self.motor2_dial.setWrapping(True)
        self.motor2_dial.setNotchesVisible(True)
        self.motor2_dial.setInvertedAppearance(True)
        self.motor2_dial.dialValueWhileDragging.connect(self.set_motor2_speed)

        self.grid_layout: QGridLayout = QGridLayout()
        self.grid_layout.addWidget(self.canvas_view, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.connect_button, 1, 0)
        self.grid_layout.addWidget(self.disconnect_button, 1, 1)
        self.grid_layout.addWidget(self.motor1_dial, 2, 0)
        self.grid_layout.addWidget(self.motor2_dial, 2, 1)

        central_widget: QWidget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.drawer: Drawer = Drawer(self.robot, self.canvas_scene)
        self.drawer.draw()
        self.canvas_scene.set_updater(self.update_gui)

    def update_gui(self) -> None:
        self.drawer.draw()
        self.motor1_dial.setValue(int(self.robot.phi[0] / 3.14 * 180))
        self.motor2_dial.setValue(int(self.robot.phi[1] / 3.14 * 360))

    @Slot()
    def connect(self) -> None:
        print("Connect button clicked")

    @Slot()
    def disconnect(self) -> None:
        print("Disconnect button clicked")

    @Slot(int)
    def set_motor1_speed(self, value) -> None:
        print("Motor 1 speed set to:", value)
        self.robot.set_phi_1(value / 180 * 3.14)
        self.drawer.draw()

    @Slot(int)
    def set_motor2_speed(self, value) -> None:
        print("Motor 2 speed set to:", value)
        self.robot.set_phi_2(value / 180 * 3.14)
        self.drawer.draw()