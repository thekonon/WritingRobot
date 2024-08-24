import logging

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QGridLayout
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QPen, QColor

from .control_panel import ControlPanel
from .drawing_widget import DrawingWidget
from ..logger import *
from .. import Robot

class RobotGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._setup_loger()
        self.logger.info("Robot GUI initializing started")
        
        self._create_app()
        self._create_robot()
        self._plot_robot()
    
    def _create_robot(self):
        self.robot: Robot = Robot()
        self.drawing_widget.set_robot(self.robot)
    
    def _plot_robot(self):
        self.drawing_widget.draw_robot()
    
    def _create_app(self):
        # Create the central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout: QVBoxLayout = QVBoxLayout(self.central_widget)

        # Create a frame
        self.frame_draw = QFrame()
        self.frame_draw.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.frame_draw)
        
        # Create a DrawingWidget and add it to the frame_draw
        self.drawing_widget: DrawingWidget = DrawingWidget()
        frame_draw_layout = QVBoxLayout(self.frame_draw)
        frame_draw_layout.addWidget(self.drawing_widget)      
        
        # Lower part of the GUI
        self.lower_hbox: QHBoxLayout = QHBoxLayout()
        self.layout.addLayout(self.lower_hbox)
        
        # Create a frame
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.lower_hbox.addWidget(self.frame)
        
        # Create a frame
        self.frame2 = QFrame()
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.lower_hbox.addWidget(self.frame2)

        # Set the layout for the frame
        self.control_panel = ControlPanel()
        self.control_panel_2 = ControlPanel()
        self.frame.setLayout(self.control_panel)
        self.frame2.setLayout(self.control_panel_2)

        # Set the main window properties
        self.setWindowTitle("Writing Robot")
        self.resize(800, 800)
        self.show()
        
        
    
    def _setup_loger(self):
        self.logger = logging.getLogger("RobotGUI")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(get_logger_console_handler())
        self.logger.addHandler(get_logger_file_handler())
        # self.logger.log(logging.ERROR, "FAILED")
        self.logger.log(logging.INFO, "RobotGUI logger started")
        
if __name__ == "__main__":
    print("Running")