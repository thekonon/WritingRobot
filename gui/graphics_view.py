from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRectF

class GridGraphicsView(QGraphicsView):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)
        self.zoom_factor = 1.25
        self.setRenderHint(QPainter.Antialiasing)

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        grid_color = QColor(200, 200, 200)
        painter.setPen(grid_color)
        grid_size = 20
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        for x in range(left - (left % grid_size), right, grid_size):
            painter.drawLine(x, top, x, bottom)

        for y in range(top - (top % grid_size), bottom, grid_size):
            painter.drawLine(left, y, right, y)
