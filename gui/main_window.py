import sys
import datetime
import os
import gui.constants as constants
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QApplication
from PySide6.QtCore import Slot, Signal
from gui.mechanics.robot import Robot
from gui.graphics import MyGraphicsScene, GridGraphicsView, Drawer
from gui.motor_dial import MotorDial
from gui.control._tools import CANCommunicationHandler, MotorDataFrame
from gui.control._helpers import Calculations
from math import cos, sin, pi
from typing import List, Callable

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app: QApplication = app
        
        self._log("Creating robot started")
        self.robot: Robot = Robot()

        self._set_up_app()
        self._create_widgets()
        self._set_up_drawer()
        self._set_up_communication()
        self._add_widgets()

        self.update_gui()

    def _set_up_app(self) -> None:
        """
        Create a basic window, set the dimensions
        
        Set ups:
            - Title
            - Geometry
        """
        self._log("Setting up the application")
        screen_geometry = self.app.primaryScreen().geometry()
        screen_width: int = screen_geometry.width()
        screen_height: int = screen_geometry.height()

        self.setWindowTitle("RobotController")
        self.setGeometry((screen_width-constants.App.APP_WIDTH)//2,
                         (screen_height-constants.App.APP_HEIGHT)//2,
                         constants.App.APP_WIDTH,
                         constants.App.APP_HEIGHT)

    def _create_widgets(self) -> None:
        """
        Add the widgets to the window
        """
        self._log("Creating widgets started")

        self.main_widget = QWidget()

        # Creating layout for main_widget
        self.main_layout = QVBoxLayout()

        # Adding a single button to main_layout
        self.graphics_scene: MyGraphicsScene = MyGraphicsScene(self.robot)
        self.graphics_view: GridGraphicsView = GridGraphicsView(
            self.graphics_scene)

        # Creating layout for buttons
        self.motor_dial_layout = QHBoxLayout()

        # Adding Motor dial 1
        self.motor_dial_1: MotorDial = \
            self._create_motor_dial(
                10, 
                self.set_motor1_speed
                )

        # Adding Motor dial 2
        self.motor_dial_2: MotorDial = \
            self._create_motor_dial(
                10, 
                self.set_motor2_speed
                )

        # Adding Connect / disconned buttons
        self.button_layout = QVBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconned")
        self.connect_button.setMaximumWidth(200)
        self.connect_button.setStyleSheet("padding: 20px;")
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button.setMaximumWidth(200)
        self.disconnect_button.setStyleSheet("padding: 20px;")
        self.disconnect_button.clicked.connect(self.disconnect)

    def _add_widgets(self):
        self._log("Creating app - adding widgets")
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.graphics_view)
        self.motor_dial_layout.addWidget(self.motor_dial_1)
        self.motor_dial_layout.addWidget(self.motor_dial_2)
        self.button_layout.addWidget(self.connect_button)
        self.button_layout.addWidget(self.disconnect_button)
        self.motor_dial_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.motor_dial_layout)

    def _set_up_drawer(self):
        self._log("Setting up drawer")
        self.drawer = Drawer(self.robot, self.graphics_scene)
        self.graphics_scene.set_updater(self.update_gui)

    def _set_up_communication(self):
        self.can_communication: CANCommunicationHandler = CANCommunicationHandler()
        self.data: MotorDataFrame = MotorDataFrame(total_motors=2)

    def _create_motor_dial(self, value: float, slot_function: Callable) -> MotorDial:
        dial: MotorDial = MotorDial()
        dial.setMinimum(0)
        dial.setMaximum(360)
        dial.setValue(int(value / 3.14 * 180))
        dial.setWrapping(True)
        dial.setNotchesVisible(True)
        dial.setInvertedAppearance(True)
        dial.dialValueWhileDragging.connect(slot_function)
        # Adjust the size of the dial
        dial.setFixedSize(200, 200)
        return dial

    def update_gui(self) -> None:
        self.drawer.draw()
        motor_1_value: int = int(self.robot.phi[0] / 3.14 * 180)
        motor_2_value: int = int(self.robot.phi[1] / 3.14 * 360)
        self.motor_dial_1.setValue(motor_1_value)
        self.motor_dial_2.setValue(motor_2_value)
        self.can_communication.motor_data_frame.set_data(
            Calculations.map_to_data(motor_1_value), motor=0)
        self.can_communication.motor_data_frame.set_data(
            Calculations.map_to_data(motor_2_value), motor=1)
        try:
            self.can_communication.send_data("MotorDataFrame")
        except ValueError as ex:
            pass

    @Slot()
    def connect(self) -> None:
        self._log("Connect button clicked")
        try:
            self.can_communication.init_communication()
        except NotImplementedError as ex:
            self._log("This OS is not supported, run it on Raspberry")

    @Slot()
    def disconnect(self) -> None:
        self._log("Disconnect button clicked")
        self.can_communication.end_communication()

    @Slot(int)
    def set_motor1_speed(self, value) -> None:
        self.robot.set_phi_1(value*3.14/180)
        self.drawer.draw()
        self.can_communication.motor_data_frame.set_data(
            Calculations.map_to_data(value), motor=0)
        self.can_communication.send_data("MotorDataFrame")

    @Slot(int)
    def set_motor2_speed(self, value) -> None:
        self.robot.set_phi_2(value*3.14/180)
        self.drawer.draw()
        self.can_communication.motor_data_frame.set_data(
            Calculations.map_to_data(value), motor=1)
        self.can_communication.send_data("MotorDataFrame")

    def _log(self, message: str) -> None:
        current_time: datetime.time = datetime.datetime.now().time()
        formatted_time: str = current_time.strftime("%H:%M:%S.%f")[:10]
        file_name: str = os.path.basename(__file__)
        print(f"{file_name}, time: {formatted_time}: {message}")
