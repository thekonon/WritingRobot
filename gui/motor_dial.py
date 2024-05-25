from PySide6.QtWidgets import QDial
from PySide6.QtCore import Signal, Qt

class MotorDial(QDial):
    dialValueWhileDragging = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.is_mouse_pressed = False

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
