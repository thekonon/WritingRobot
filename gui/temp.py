import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Layout Example")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Creating layout for main_widget
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Creating layout for buttons
        button_layout = QHBoxLayout()

        # Adding buttons to button_layout
        button1 = QPushButton("Button 1")
        button_layout.addWidget(button1)

        button2 = QPushButton("Button 2")
        button_layout.addWidget(button2)

        # Adding button_layout to main_layout
        main_layout.addLayout(button_layout)

        # Adding a single button to main_layout
        button3 = QPushButton("Button 3")
        main_layout.addWidget(button3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
