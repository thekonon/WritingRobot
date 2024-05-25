from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import QPointF, Qt, QRectF
from gui.mechanics.robot import Robot
from typing import List
from math import cos, sin

class Drawer:
    def __init__(self, robot: Robot, canvas_scene) -> None:
        self.robot = robot
        self.scene = canvas_scene

    def draw(self) -> None:
        self.scene.clear()
        lengths = self.robot.lengths
        phis = self.robot.phi
        self.draw_line(QPointF(0, 0), QPointF(lengths[0] * cos(phis[0]), lengths[0] * sin(phis[0])))
        self.draw_line(QPointF(lengths[4], 0), QPointF(lengths[4] + lengths[1] * cos(phis[1]), lengths[1] * sin(phis[1])))
        self.draw_line(QPointF(lengths[0] * cos(phis[0]), lengths[0] * sin(phis[0])), QPointF(lengths[0] * cos(phis[0]) + lengths[2] * cos(phis[2]), lengths[0] * sin(phis[0]) + lengths[2] * sin(phis[2])))
        self.draw_line(QPointF(lengths[4] + lengths[1] * cos(phis[1]), lengths[1] * sin(phis[1])), QPointF(lengths[4] + lengths[1] * cos(phis[1]) + lengths[3] * cos(phis[3]), lengths[1] * sin(phis[1]) + lengths[3] * sin(phis[3])))
        self.draw_limit_circles()

    def draw_line(self, start_point: QPointF, end_point: QPointF) -> None:
        line = QGraphicsLineItem(start_point.x(), -start_point.y(), end_point.x(), -end_point.y())
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(3)
        line.setPen(pen)
        self.scene.addItem(line)

    def draw_limit_circles(self) -> None:
        mid_point_1 = QPointF(0, 0)
        mid_point_2 = QPointF(50, 0)
        radius = QPointF(-200, -200)
        rect_1 = QRectF(mid_point_1 - radius, mid_point_1 + radius)
        rect_2 = QRectF(mid_point_2 - radius, mid_point_2 + radius)
        self.draw_circle(rect_1)
        self.draw_circle(rect_2)

    def draw_circle(self, rect: QRectF) -> None:
        circle = QGraphicsEllipseItem(rect)
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)
        pen.setStyle(Qt.DashLine)
        circle.setPen(pen)
        self.scene.addItem(circle)
