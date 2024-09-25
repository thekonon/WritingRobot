from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
import pyqtgraph as pg
from PySide6.QtCore import QPoint
import numpy as np
from .. import Robot
from ..logger import *

class DrawingWidget(QWidget):
    def __init__(self, parent=None):
        self._setup_loger()
        self.logger.info("Drawing object beeing created")
        super().__init__(parent)
        self.setMinimumSize(200, 200)  # Set a minimum size for the drawing widget
        
        # Create a PlotWidget from PyQtGraph
        self.plot_widget = pg.PlotWidget(background='White')
        self.plot_widget.setLabel('left', 'Y')
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setXRange(-150, 200, padding=0)
        self.plot_widget.setYRange(-50, 300, padding=0)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        
        # Set up layout and add the PlotWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Hold references to plot items
        self.lines = []
        self.circles = []
        
        self.is_mouse_pressed = False
        
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_dragged)
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_pressed)
        
        self.limits = None
        
        
    
    def set_robot(self, robot: Robot):
        self.robot: Robot = robot
        self._draw_limits()
    
    def draw_robot(self):        
        self._clear_plot()
        
        points: list = [QPoint(*point) for point in self.robot.get_points()]
        
        self.plot_line(points[0], points[1], {})
        self.plot_line(points[1], points[2], {})
        self.plot_line(points[3], points[4], {})
        self.plot_line(points[4], points[5], {})
        
        self.plot_circle(QPoint(0, 0), self.robot.settings.LENGTHS[0], {})
        self.plot_circle(QPoint(self.robot.settings.LENGTHS[4], 0), self.robot.settings.LENGTHS[2], {})
        
        
    
    def _draw_limits(self):
        if self.limits == None:
            self.limits = [QPoint(*point) for point in self.robot.get_limits()]
        
        for i in range(len(self.limits) - 1):
            self.plot_line(self.limits[i], self.limits[i + 1], {}, add_to_lines=False)
            
        self.plot_circle(QPoint(0,0), self.robot.settings.LENGTHS[0]+self.robot.settings.LENGTHS[1], {"dash": [5, 5]})
        self.plot_circle(QPoint(self.robot.settings.LENGTHS[4],0), self.robot.settings.LENGTHS[2]+self.robot.settings.LENGTHS[3], {"dash": [30, 30]})

    def plot_line(self, start_point: QPoint, end_point: QPoint, line_settings: dict, add_to_lines = True):
        """Add a line to be drawn."""
        # Convert QPoint to tuples
        start = (start_point.x(), start_point.y())
        end = (end_point.x(), end_point.y())
        
        # Create the line plot
        pen_color = line_settings.get('color', 'red')
        pen_width = line_settings.get('width', 2)
        pen = pg.mkPen(color=pen_color, width=pen_width)
        line = pg.PlotDataItem([start[0], end[0]], [start[1], end[1]], pen=pen)
        
        # Add to plot
        self.plot_widget.addItem(line)
        if add_to_lines:
            self.lines.append(line)

    def plot_circle(self, mid_point: QPoint, radius: int, line_settings: dict, starting_angle: float = 0, ending_angle=2*np.pi, add_to_circles=True):
        """Add a circle to be drawn."""
        # Convert QPoint to tuple
        center = (mid_point.x(), mid_point.y())
        
        # Create the pen with pyqtgraph directly
        pen_color = line_settings.get('color', 'black')
        pen_width = line_settings.get('width', 2)
        dash_pattern = line_settings.get('dash', None)
        
        # Create the pyqtgraph pen directly with dash pattern
        if dash_pattern:
            pen = pg.mkPen(color=pen_color, width=pen_width, style=Qt.CustomDashLine)
            pen.setDashPattern(dash_pattern)
        else:
            pen = pg.mkPen(color=pen_color, width=pen_width)
        
        # Create the parametric equation for the circle
        t = np.linspace(starting_angle, ending_angle, 100)
        x = center[0] + radius * np.cos(t)
        y = center[1] + radius * np.sin(t)
        
        # Create the PlotCurveItem with the customized pen
        circle_item = pg.PlotCurveItem(x, y, pen=pen)
        
        # Add to plot
        self.plot_widget.addItem(circle_item)
        if add_to_circles:
            self.circles.append(circle_item)
    
    def _clear_plot(self):
        """Clears all the lines and circles from the plot."""
        # Remove all line items
        for line in self.lines:
            self.plot_widget.removeItem(line)
        self.lines.clear()

        # Remove all circle items
        for circle in self.circles:
            self.plot_widget.removeItem(circle)
        self.circles.clear()

    
    def on_mouse_dragged(self, pos):
        """Slot to handle mouse movement during dragging."""
        if self.is_mouse_pressed:
            # Map the scene position to the plot coordinates
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x = mouse_point.x()
            y = mouse_point.y()
            self.robot.set_end_point([x, y])
            self.draw_robot()
        
    def on_mouse_pressed(self, event):
        """Slot to handle mouse press and release events."""
        if event.button().name == 'LeftButton' and event.button().value == 1:  # Left mouse button pressed
            self.is_mouse_pressed = not self.is_mouse_pressed

    def _setup_loger(self):
        self.logger = logging.getLogger("RobotGUI")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(get_logger_console_handler())
        self.logger.addHandler(get_logger_file_handler())
        # self.logger.log(logging.ERROR, "FAILED")
        self.logger.log(logging.INFO, "RobotGUI logger started")