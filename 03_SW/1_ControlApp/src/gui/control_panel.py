from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QDial, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from enum import Enum


class ControlPanelTypes(Enum):
    BUTTONS = 1
    KNOBS = 2


class ControlPanelFactory:
    @staticmethod
    def create(type: ControlPanelTypes, parent: QWidget | None = None) -> QHBoxLayout:
        match type:
            case ControlPanelTypes.BUTTONS:
                return ControlPanelButtons(parent)
            case ControlPanelTypes.KNOBS:
                return ControlPanelKnobs(parent)
            case _:
                raise ValueError("Uknown control panel name")


class ControlPanelButtons(QHBoxLayout):
    def __init__(self, parent: QWidget | None = None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        self.connect_button: QPushButton = QPushButton("Connect")
        self.disconnect_button: QPushButton = QPushButton("Disconnect")
        self.init_widgets()

    def init_widgets(self):
        self.addWidget(self.connect_button)
        self.addWidget(self.disconnect_button)


class ControlPanelKnobs(QHBoxLayout):
    def __init__(self, parent: QWidget | None = None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        # Two knobs
        self.knob_left: QDial = QDial()
        self.knob_right: QDial = QDial()

        # Optional: limits, steps
        self.knob_left.setRange(0, 100)
        self.knob_right.setRange(0, 100)

        self.knob_left.setNotchesVisible(True)
        self.knob_right.setNotchesVisible(True)

        # UI initialization
        self.init_widgets()

    def _wrap_knob(self, knob: QDial, text: str) -> QWidget:
        """Creates a small vertical layout: knob + label."""
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(knob)
        layout.addWidget(label)

        return wrapper

    def init_widgets(self):
        # Add two labeled knobs
        self.addWidget(self._wrap_knob(self.knob_left, "Left Knob"))
        self.addWidget(self._wrap_knob(self.knob_right, "Right Knob"))
