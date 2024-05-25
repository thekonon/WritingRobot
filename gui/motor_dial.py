from PySide6.QtWidgets import QDial
from PySide6.QtCore import Signal

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
        # event.buttons().value == 1 == leftButton
        if self.is_mouse_pressed and event.buttons().value == 1:
            self.dialValueWhileDragging.emit(self.value())
        super().mouseMoveEvent(event)
