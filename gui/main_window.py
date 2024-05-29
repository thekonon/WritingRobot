import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot, Signal
from gui.mechanics.robot import Robot
from gui.graphics import MyGraphicsScene, GridGraphicsView, Drawer
from gui.motor_dial import MotorDial
from math import cos, sin, pi
from typing import List, Callable
from .control._tools import CANCommunicationHandler, MotorDataFrame
from .control._helpers import Calculations

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.robot: Robot = Robot()
        self.can_communication: CANCommunicationHandler = CANCommunicationHandler()
        self.data: MotorDataFrame = MotorDataFrame(total_motors=2)

        self.setWindowTitle("RobotController")
        self.setGeometry(100, 100, 600, 600)

        self.canvas_scene: MyGraphicsScene = MyGraphicsScene(self.robot)
        self.canvas_view: GridGraphicsView = GridGraphicsView(self.canvas_scene)
        self.canvas_view.setScene(self.canvas_scene)

        self.connect_button: QPushButton = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button: QPushButton = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)

        self.motor1_dial: MotorDial = self.create_motor_dial(self.robot.phi[0], self.set_motor1_speed)
        self.motor2_dial: MotorDial = self.create_motor_dial(self.robot.phi[1], self.set_motor2_speed)

        self.grid_layout: QGridLayout = QGridLayout()
        self.add_widgets_to_grid_layout()

        central_widget: QWidget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.drawer: Drawer = Drawer(self.robot, self.canvas_scene)
        self.drawer.draw()
        self.canvas_scene.set_updater(self.update_gui)

    def add_widgets_to_grid_layout(self) -> None:
        self.grid_layout.addWidget(self.canvas_view, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.connect_button, 1, 0)
        self.grid_layout.addWidget(self.disconnect_button, 1, 1)
        self.grid_layout.addWidget(self.motor1_dial, 2, 0)
        self.grid_layout.addWidget(self.motor2_dial, 2, 1)

    def create_motor_dial(self, value: float, slot_function: Callable) -> MotorDial:
        dial: MotorDial = MotorDial()
        dial.setMinimum(0)
        dial.setMaximum(360)
        dial.setValue(int(value / 3.14 * 180))
        dial.setWrapping(True)
        dial.setNotchesVisible(True)
        dial.setInvertedAppearance(True)
        dial.dialValueWhileDragging.connect(slot_function)
        # Adjust the size of the dial
        dial.setFixedSize(100, 100)
        return dial

    def update_gui(self) -> None:
        self.drawer.draw()
        self.motor1_dial.setValue(int(self.robot.phi[0] / 3.14 * 180))
        self.motor2_dial.setValue(int(self.robot.phi[1] / 3.14 * 360))

    @Slot()
    def connect(self) -> None:
        print("Connect button clicked")
        self.can_communication.init_communication()
        

    @Slot()
    def disconnect(self) -> None:
        print("Disconnect button clicked")
        self.can_communication.end_communication()
        

    @Slot(int)
    def set_motor1_speed(self, value: float) -> None:
        print("Motor 1 speed set to:", value)
        self.robot.set_phi_1(value / 180 * 3.14)
        self.drawer.draw()
        self.can_communication.motor_data_frame.set_data(Calculations.map_to_data(value), motor = 0)
        print("Sending data")
        self.can_communication.send_data("MotorDataFrame")
        
        

    @Slot(int)
    def set_motor2_speed(self, value: float) -> None:
        print("Motor 2 speed set to:", value)
        self.robot.set_phi_2(value / 180 * 3.14)
        self.drawer.draw()
        self.can_communication.motor_data_frame.set_data(Calculations.map_to_data(value), motor = 1)
        print("Sending data")
        self.can_communication.send_data("MotorDataFrame")
