from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from typing import Callable
from gui.mechanics.robot import Robot

class MyGraphicsScene(QGraphicsScene):
    def __init__(self, robot: Robot) -> None:
        super().__init__()
        self.robot = robot
        self.on_left_hold = False
        self.on_right_hold = False
        self.last_pos = QPointF()

    def set_updater(self, updater: Callable) -> None:
        self.updater = updater

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.on_left_hold = True
            self.last_pos = event.scenePos()
            self.update_robot_position(event.scenePos())
            self.updater()
        elif event.button() == Qt.RightButton:
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
            delta = event.scenePos() - self.last_pos
            self.last_pos = event.scenePos()
            self.setSceneRect(self.sceneRect().translated(-delta.x(), -delta.y()))
        super().mouseMoveEvent(event)

    def update_robot_position(self, pos) -> None:
        self.robot.r_m = [pos.x(), -pos.y()]
