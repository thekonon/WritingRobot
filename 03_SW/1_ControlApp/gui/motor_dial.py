from PySide6.QtWidgets import QDial, QSizePolicy
from PySide6.QtCore import Signal

class MotorDial(QDial):
    dialValueWhileDragging: Signal = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.is_mouse_pressed: bool = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # type: ignore

    def mousePressEvent(self, event) -> None:
        self.is_mouse_pressed = True
        self.dialValueWhileDragging.emit(self.value())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.is_mouse_pressed = False
        self.dialValueWhileDragging.emit(self.value())
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.is_mouse_pressed and event.buttons().value == 1:
            self.dialValueWhileDragging.emit(self.value())
        super().mouseMoveEvent(event)

    def resizeEvent(self, event) -> None:
        # Adjust the size of the dial
        min_size = min(event.size().width(), event.size().height())
        self.setMinimumSize(min_size, min_size)
        self.setMaximumSize(min_size, min_size)
        super().resizeEvent(event)