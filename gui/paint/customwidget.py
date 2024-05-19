from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
import random

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        
        self.lines = [[0, 0, 100, 100] for _ in range(5)]  # Initialize lines
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lines)
        self.timer.start(50)  # Update every 50ms
        
        self.setMinimumSize(500, 200)
        # self.setFixedSize(200, 500)

    def update_lines(self):
        for line in self.lines:
            line[0] += random.randint(-5, 5)  # Random movement
            line[1] += random.randint(-5, 5)
            line[2] += random.randint(-5, 5)
            line[3] += random.randint(-5, 5)
        
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.fillRect(self.rect(), QBrush(QColor(255, 0, 0)))
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        
        for line in self.lines:
            painter.drawLine(*line)
