from .mechanics.robot import Robot
from PySide6.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsView, QGraphicsEllipseItem
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPointF, Slot, QRectF
from math import cos, sin, pi
from typing import List, Callable

class GridGraphicsView(QGraphicsView):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)
        self.zoom_factor: float = 1.25  # Zoom factor for each zoom step
        self.setRenderHint(QPainter.Antialiasing)
    
    def wheelEvent(self, event) -> None:
        # Zoom in or out depending on the direction of the wheel event
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        
        # Set grid color and style
        grid_color: QColor = QColor(200, 200, 200)
        painter.setPen(grid_color)
        
        # Define grid spacing
        grid_size: int = 20
        
        # Get the bounds of the scene
        left: int =     int(rect.left())
        right: int =    int(rect.right())
        top: int =      int(rect.top())
        bottom: int =   int(rect.bottom())
        
        # Draw vertical grid lines
        for x in range(left - (left % grid_size), right, grid_size):
            painter.drawLine(x, top, x, bottom)
        
        # Draw horizontal grid lines
        for y in range(top - (top % grid_size), bottom, grid_size):
            painter.drawLine(left, y, right, y)



class MyGraphicsScene(QGraphicsScene):
    def __init__(self, robot: Robot) -> None:
        super().__init__()
        self.robot: Robot = robot
        self.on_left_hold: bool = False
        self.on_right_hold: bool = False
        self.last_pos: QPointF = QPointF()

    def set_updater(self, updater: Callable) -> None:
        self.updater: Callable = updater
    
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            # Left mouse button clicked
            self.on_left_hold = True
            self.last_pos = event.scenePos()
            self.update_robot_position(event.scenePos())
            self.updater()
            
        elif event.button() == Qt.RightButton:
            # Right mouse button clicked
            self.on_right_hold = True
            self.last_pos = event.scenePos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.on_left_hold = False
        elif event.button() == Qt.RightButton:
            self.on_right_hold = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.on_left_hold:
            self.update_robot_position(event.scenePos())
            self.updater()
            self.last_pos = event.scenePos()
        elif self.on_right_hold:
            delta: QPointF = event.scenePos() - self.last_pos
            self.last_pos = event.scenePos()
            self.setSceneRect(self.sceneRect().translated(-delta.x(), -delta.y()))
        super().mouseMoveEvent(event)

    def update_robot_position(self, pos) -> None:
        self.robot.r_m = [pos.x(), -pos.y()]
      

class Drawer:
    def __init__(self, robot: Robot, canvas_scene: MyGraphicsScene) -> None:
        self.robot: Robot           = robot
        self.scene: MyGraphicsScene  = canvas_scene
    
    def draw(self) -> None:
        self.scene.clear()
        lengths: tuple = self.robot.lengths
        phis: List[float] = self.robot.phi
        # Line 1
        x1: float = lengths[0]*cos(phis[0])
        y1: float = lengths[0]*sin(phis[0])
        start_point: QPointF    = QPointF(0, 0)
        end_point: QPointF      = QPointF(x1, y1)
        self.draw_line(start_point, end_point)
        
        # Line 2
        x20: float = lengths[4]
        y20: float = 0
        x2: float = x20 + lengths[1]*cos(phis[1])
        y2: float = y20 + lengths[1]*sin(phis[1])
        start_point = QPointF(x20, y20)
        end_point = QPointF(x2, y2)
        self.draw_line(start_point, end_point)
        
        # Line 3
        x3: float = x1 + lengths[2]*cos(phis[2])
        y3: float = y1 + lengths[2]*sin(phis[2])
        start_point: QPointF    = QPointF(x1, y1)
        end_point: QPointF      = QPointF(x3, y3)
        self.draw_line(start_point, end_point)
        
        # Line 4
        x4: float = x2 + lengths[3]*cos(phis[3])
        y4: float = y2 + lengths[3]*sin(phis[3])
        start_point: QPointF    = QPointF(x2, y2)
        end_point: QPointF      = QPointF(x4, y4)
        self.draw_line(start_point, end_point)
        
        self.draw_limit_circles()
        
        
    def draw_line(self, start_point: QPointF, end_point: QPointF) -> None:
        line: QGraphicsLineItem = QGraphicsLineItem(
            start_point.x(), 
            -start_point.y(), 
            end_point.x(), 
            -end_point.y())
        
        pen = QPen(QColor(0, 0, 0))  # Set color to black
        pen.setWidth(3)
        line.setPen(pen)
        
        self.scene.addItem(line)
        
    def draw_limit_circles(self) -> None:
        mid_point_1: QPointF = QPointF(0, 0)
        mid_point_2: QPointF = QPointF(50, 0)
        radius: QPointF = QPointF(-200, -200)
        rect_1: QRectF = QRectF(mid_point_1-radius, mid_point_1+radius)
        rect_2: QRectF = QRectF(mid_point_2-radius, mid_point_2+radius)
        
        
        # Draw the first circle at (0, 0)
        circle1: QGraphicsEllipseItem = QGraphicsEllipseItem(rect_1)  # Circle centered at (0, 0) with radius 100
        pen1: QPen = QPen(QColor(255, 0, 0))  # Red color for the circle
        pen1.setWidth(3)
        pen1.setStyle(Qt.DashLine)  # Dashed line style
        circle1.setPen(pen1)
        self.scene.addItem(circle1)

        # Draw the second circle at (0, 50)
        circle2: QGraphicsEllipseItem = QGraphicsEllipseItem(rect_2)  # Circle centered at (0, 50) with radius 100
        pen2: QPen = QPen(QColor(255, 0, 0))  # Red color for the circle
        pen2.setWidth(3)
        pen2.setStyle(Qt.DashLine)  # Dashed line style
        circle2.setPen(pen2)
        self.scene.addItem(circle2)
        
        
    def draw_pentagram(self) -> None:
        center: QPointF = QPointF(300, 300)
        radius: float = min(600, 600) / 3
        angle_offset: float = -pi / 2  # Start from the top
        angle_step: float = 2 * pi / 5  # Divide the circle into 5 equal parts

        # Draw 5 lines forming a pentagram
        for i in range(5):
            start_point: QPointF = QPointF(
                center.x() + radius * cos(angle_offset + i * angle_step),
                center.y() + radius * sin(angle_offset + i * angle_step)
            )
            end_point: QPointF = QPointF(
                center.x() + radius * cos(angle_offset + (i + 2) * angle_step),
                center.y() + radius * sin(angle_offset + (i + 2) * angle_step)
            )
            line: QGraphicsLineItem = QGraphicsLineItem(start_point.x(), start_point.y(), end_point.x(), end_point.y())
            self.scene.addItem(line)
            