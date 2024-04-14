import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from my import Ui_MainWindow  # Import the generated UI class
from _tools import CANCommunicationHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.update_time_threshold = .1 #in s
        
        # CAN Communication object
        self.communication_handler = CANCommunicationHandler()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals and slots
        self.ui.connectButton.clicked.connect(self.connect_function)
        self.ui.pushButton.clicked.connect(self.clear_log)
        self.ui.dialButton.valueChanged.connect(self.button_moved)
        
        self._time_since_last_update = time.time()
        
        self._min_value = self.ui.dialButton.minimum()
        self._max_value = self.ui.dialButton.maximum()
        self._remapped_min = -360
        self._remapped_max = 360

    def button_moved(self, value):
        if (time.time()-self._time_since_last_update)<self.update_time_threshold:
            return 0
        self._time_since_last_update = time.time()
        
        mapped_val = self._map_value(value)
        data = self._value_to_hex(mapped_val)
        self.communication_handler.motor_data_frame.set_data(data)
        self.communication_handler.send_data('MotorDataFrame')
        self.add_to_log(str(value))
        
    
    def connect_function(self):
        self.communication_handler.init_communication()
        self.add_to_log("Connection established")
    
    def disconnect_function(self):
        self.communication_handler.end_communication()
        self.add_to_log("Disconnected")

    def clear_log(self):
        self.ui.logWindow.clear()
    
    def add_to_log(self, new_text: str):
        old_text = self.ui.logWindow.toPlainText()
        new_text_to_be_set = old_text + "\n"+ new_text
        if new_text_to_be_set.startswith("\n"):
            new_text_to_be_set = new_text_to_be_set[1:]
        self.ui.logWindow.setText(new_text_to_be_set)
        self._scroll_to_bottom()
    
    def _map_value(self, value):
        total_size = self._max_value - self._min_value
        procent = value/total_size
        total_new = self._remapped_max-self._remapped_min
        return self._remapped_min+procent*total_new
    
    def _value_to_hex(self, value: int):
        # 1st byte      - sign 0 - +
        # 2nd/3rd byte  - value before decimal
        # 4th byte      - after decimal value
        # e.g. 347.36 -> [0, 1, 91, 36]
        before_decimal = abs(int(value))
        after_decimal = int(abs(value) % 1 * 100)  # Extracting the first two decimal digits
        if before_decimal > 2 ** 16:
            raise ValueError("Too large number to be sent")
        if after_decimal > 2 ** 8:
            raise ValueError("Too large number to be sent")
        hex_sign = "00" if value >= 0 else "01"  # Padding sign to 2 characters

        hex_before_decimal = format(before_decimal, '04x')  # Padding to 4 characters
        hex_after_decimal = format(after_decimal, '02x')  # Padding to 2 characters

        # Returning list of integers representing hex values
        return [int(hex_sign, 16), int(hex_before_decimal[:2], 16), int(hex_before_decimal[2:], 16), int(hex_after_decimal, 16)]
        
    
    def _scroll_to_bottom(self):
        scrollbar = self.ui.logWindow.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
