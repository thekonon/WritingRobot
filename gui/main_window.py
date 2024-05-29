import sys
import datetime
import win32api
import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot, Signal
from gui.mechanics.robot import Robot
from gui.graphics import MyGraphicsScene, GridGraphicsView, Drawer
from gui.motor_dial import MotorDial
from math import cos, sin, pi
from typing import List, Callable


class Constants:
    APP_WIDTH: int = 1800
    APP_HEIGHT: int = 1000

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._log("Creating robot started")
        self.robot: Robot = Robot()
        
        self._set_up_app()
        self._create_widgets()
        
        self.setCentralWidget(self.central_widget)
        self.add_widgets_to_grid_layout()
        
    def _set_up_app(self) -> None:
        self._log("Setting up the application")
        screen_width: int = win32api.GetSystemMetrics(0)
        screen_height: int = win32api.GetSystemMetrics(1)

        self.setWindowTitle("RobotController")
        self.setGeometry((screen_width-Constants.APP_WIDTH)//2,
                         (screen_height-Constants.APP_HEIGHT)//2, 
                         Constants.APP_WIDTH,
                         Constants.APP_HEIGHT)

    def _create_widgets(self) -> None:
        self._log("Creating widgets started")
        self.central_widget: QWidget = QWidget()
        self.central_grid: QGridLayout = QGridLayout(self.central_widget)
        self.central_widget.setMinimumWidth(Constants.APP_WIDTH)
        
        self.graphics_scene: MyGraphicsScene|None = None #MyGraphicsScene()
        self.graphics_view: GridGraphicsView = GridGraphicsView(self.graphics_scene)
        self.motor_dial_1: MotorDial = self.create_motor_dial(10, self.set_motor1_speed)
        # self.motor_dial_2: MotorDial = self.create_motor_dial(10, self.set_motor2_speed)
        
        # self.graphics_scene.set_robot(self.robot)
        
    
    def add_widgets_to_grid_layout(self) -> None:
        self.central_grid.addWidget(self.graphics_view, 0, 0, 1, 2)
        self.central_grid.addWidget(self.motor_dial_1, 1, 0)
        # self.central_grid.addWidget(self.motor_dial_2, 1, 1)

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
        dial.setFixedSize(200, 200)
        return dial

    def update_gui(self) -> None:
        pass

    @Slot()
    def connect(self) -> None:
        self._log("Connect button clicked")

    @Slot()
    def disconnect(self) -> None:
        self._log("Disconnect button clicked")

    @Slot(int)
    def set_motor1_speed(self, value) -> None:
        pass

    @Slot(int)
    def set_motor2_speed(self, value) -> None:
        pass
    
    def _log(self, message: str) -> None:
        current_time: datetime.time = datetime.datetime.now().time()
        formatted_time: str = current_time.strftime("%H:%M:%S.%f")[:10]
        file_name: str = os.path.basename(__file__)
        print(f"{file_name}, time: {formatted_time}: {message}")
