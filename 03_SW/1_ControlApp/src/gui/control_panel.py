from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
        
class ControlPanel(QHBoxLayout):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.connect_button: QPushButton = QPushButton("Connect")
        self.disconnect_button: QPushButton = QPushButton("Disconnect")
        self.init_widgets()

    def init_widgets(self):
        self.addWidget(self.connect_button)
        self.addWidget(self.disconnect_button)