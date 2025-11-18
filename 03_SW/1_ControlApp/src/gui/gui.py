import logging

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from .control_panel import ControlPanelFactory, ControlPanelTypes
from .drawing_widget import DrawingWidget
from ..logger import *
from .. import Robot


class RobotGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.logger: logging.Logger = get_logger()
        self.logger.info("Robot GUI initializing started")

        # Create a DrawingWidget
        self.drawing_widget: DrawingWidget = DrawingWidget()

        self.robot: Robot

        self._create_app()
        self._create_robot()
        
        # Set a connection between drawing app and robot for sending desired position
        self.drawing_widget.set_robot(self.robot)

        self._plot_robot()

    def _create_robot(self):
        """Creates instance of robot"""
        self.robot = Robot()

    def _plot_robot(self):
        """Draws initial position of robot"""
        self.drawing_widget.draw_robot()

    def _create_app(self):
        """Creates the GUI for the app"""
        self.logger.info("App creating started")

        # Create the central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout: QVBoxLayout = QVBoxLayout(self.central_widget)

        # Create a frame
        self.frame_draw = QFrame()
        self.frame_draw.setFrameShape(QFrame.Shape.StyledPanel)
        self.layout.addWidget(self.frame_draw)

        # add drawing widget to the frame_draw
        frame_draw_layout = QVBoxLayout(self.frame_draw)
        frame_draw_layout.addWidget(self.drawing_widget)

        # Lower part of the GUI
        self.lower_hbox: QHBoxLayout = QHBoxLayout()
        self.layout.addLayout(self.lower_hbox)

        # Create a frame
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.lower_hbox.addWidget(self.frame)

        # Create a frame
        self.frame2 = QFrame()
        self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.lower_hbox.addWidget(self.frame2)

        # Set the layout for the frame
        self.control_panel = ControlPanelFactory.create(ControlPanelTypes.BUTTONS)
        self.control_panel_2 = ControlPanelFactory.create(ControlPanelTypes.KNOBS)
        self.frame.setLayout(self.control_panel)
        self.frame2.setLayout(self.control_panel_2)

        # Set the main window properties
        self.setWindowTitle("Writing Robot")
        self.resize(800, 800)
        self.show()


if __name__ == "__main__":
    print("Running")
