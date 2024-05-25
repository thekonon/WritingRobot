from PySide6.QtWidgets import QMainWindow, QPushButton, QDial, QGridLayout, QWidget
from PySide6.QtCore import Slot
from gui.drawer.drawer import Drawer
from gui.mechanics.robot import Robot
from gui.graphics_view import GridGraphicsView
from gui.graphics_scene import MyGraphicsScene
from gui.motor_dial import MotorDial

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.robot = Robot()
        self.init_ui()
        self.drawer = Drawer(self.robot, self.canvas_scene)
        self.drawer.draw()
        self.canvas_scene.set_updater(self.update_gui)

    def init_ui(self):
        self.setWindowTitle("RobotController")
        self.setGeometry(100, 100, 600, 600)

        self.canvas_scene = MyGraphicsScene(self.robot)
        self.canvas_view = GridGraphicsView(self.canvas_scene)
        self.canvas_view.setScene(self.canvas_scene)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)

        self.motor1_dial = MotorDial()
        self.setup_dial(self.motor1_dial, self.robot.phi[0], self.set_motor1_speed)

        self.motor2_dial = MotorDial()
        self.setup_dial(self.motor2_dial, self.robot.phi[1], self.set_motor2_speed)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.canvas_view, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.connect_button, 1, 0)
        self.grid_layout.addWidget(self.disconnect_button, 1, 1)
        self.grid_layout.addWidget(self.motor1_dial, 2, 0)
        self.grid_layout.addWidget(self.motor2_dial, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

    def setup_dial(self, dial, phi_value, slot):
        dial.setMinimum(0)
        dial.setMaximum(360)
        dial.setWrapping(True)
        dial.setNotchesVisible(True)
        dial.setValue(int(phi_value / 3.14 * 180))
        dial.setInvertedAppearance(True)
        dial.dialValueWhileDragging.connect(slot)

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