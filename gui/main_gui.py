import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QPushButton,
    QDial,
    QGridLayout,
    QWidget,
)
from PySide6.QtCore import Qt, Slot, Signal
from .mechanics import Robot
from .drawer import GridGraphicsView, Drawer, MyGraphicsScene
from math import cos, sin, pi
from typing import List


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.robot: Robot = Robot()

        # Set window title and size
        self.setWindowTitle("RobotController")
        self.setGeometry(100, 100, 600, 600)

        # Create QGraphicsView and QGraphicsScene for pentagram
        self.canvas_scene: QGraphicsScene = MyGraphicsScene(self.robot)
        self.canvas_view: GridGraphicsView = GridGraphicsView(self.canvas_scene)
        self.canvas_view.setScene(self.canvas_scene)

        # Create connect and disconnect buttons
        self.connect_button: QPushButton = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button: QPushButton = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)

        # Create dial for controlling motor1
        self.motor1_dial: QDial = MotorDial()
        self.motor1_dial.setMinimum(0)
        self.motor1_dial.setMaximum(360)  # Set maximum value to 360 degrees
        self.motor1_dial.setWrapping(
            True
        )  # Allow wrapping around when reaching minimum or maximum
        self.motor1_dial.setNotchesVisible(True)  # Show notches
        self.motor1_dial.setValue(int(self.robot.phi[0] / 3.14 * 180))
        self.motor1_dial.setInvertedAppearance(
            True
        )  # Invert the dial appearance to start from the bottom
        self.motor1_dial.dialValueWhileDragging.connect(self.set_motor1_speed)

        self.motor2_dial: QDial = MotorDial()
        self.motor2_dial.setMinimum(0)
        self.motor2_dial.setMaximum(360)
        self.motor2_dial.setValue(int(self.robot.phi[1] / 3.14 * 360))
        self.motor2_dial.setWrapping(
            True
        )  # Allow wrapping around when reaching minimum or maximum
        self.motor2_dial.setNotchesVisible(True)  # Show notches
        self.motor2_dial.setInvertedAppearance(
            True
        )  # Invert the dial appearance to start from the bottom
        self.motor2_dial.dialValueWhileDragging.connect(self.set_motor2_speed)

        # Create grid layout
        self.grid_layout: QGridLayout = QGridLayout()

        # Add pentagram graphics view to layout
        self.grid_layout.addWidget(self.canvas_view, 0, 0, 1, 2)

        # Add widgets to layout
        self.grid_layout.addWidget(self.connect_button, 1, 0)
        self.grid_layout.addWidget(self.disconnect_button, 1, 1)
        self.grid_layout.addWidget(self.motor1_dial, 2, 0)
        self.grid_layout.addWidget(self.motor2_dial, 2, 1)

        # Create central widget and set layout
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


class MotorDial(QDial):
    dialValueWhileDragging: Signal = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.is_mouse_pressed: bool = False

    def mousePressEvent(self, event) -> None:
        self.is_mouse_pressed = True
        self.dialValueWhileDragging.emit(self.value())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.is_mouse_pressed = False
        self.dialValueWhileDragging.emit(self.value())
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.is_mouse_pressed and event.buttons() & Qt.LeftButton:
            self.dialValueWhileDragging.emit(self.value())
        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
