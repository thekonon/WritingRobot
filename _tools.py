import can
import os
from typing import List
from enum import Enum


class BitRates(Enum):
    _125KHZ: int = 125000


class CANCommunicationHandler:
    """# CANCOmmunicationHandler
    1) Create this object
    2) Modify data
        a) obj.motor_data_frame.set_data(data)
    3) Send data via CAN BUS
    """

    def __init__(self) -> None:

        self.bus: can.bus

        # Communicatino settings
        self._BITRATE: int = BitRates["_125KHZ"]
        self._CAN_INTERFACE: str = "can0"
        self._BUS_TYPE: str = "socketcan"

        # MotorDataFrame settings
        self.motor_data_frame = MotorDataFrame()

        # State variables
        self._init_done = 0

    def send_data(self, selected_type: str):
        """Send all frames via can"""
        if not self._init_done:
            raise ValueError("Initialization needs to be done")
        types = {"MotorDataFrame": self.motor_data_frame.get_msg()}
        msg = types.get(selected_type)
        if msg:
            self.bus.send(msg)
        else:
            raise ValueError("Uknown type message selected")

    def init_communication(self):
        if os.name == "nt":
            raise NotImplementedError("Implementation for Windows not implemented")
        os.system("sudo ip link set can0 up type can bitrate 125000")
        # os.system("sudo ip link set can0 up")
        self.bus = can.interface.Bus(
            channel=self._CAN_INTERFACE, bustype=self._BUS_TYPE
        )
        self._init_done = 1

    def end_communication(self):
        self.bus.shutdown()
        os.system("sudo ip link set can0 down")


class MotorDataFrame:
    def __init__(self, total_motors: int = 1) -> None:
        # Motors to be controlled
        self.total_motors: int = total_motors

        # MSG id for motor(s) control
        self.MSG_ID: int = 0

        # MSG length - 4 bytes if only 1 motor is controlled
        self._msg_length: int = 4 if self.total_motors == 1 else 8

        # Init data to be send
        self.data: List[int] = []

        # Init msg object
        self._create_msg()

    def set_data(self, data: List[int], motor: int = 0):
        if motor:
            self.data[:4] = data
        else:
            self.data[4:] = data
        self._create_msg()

    def get_msg(self) -> can.Message:
        return self._msg

    def _create_msg(self):
        self._msg = can.Message(
            arbitration_id=self.MSG_ID, is_extended_id=False, data=self.data
        )


if __name__ == "__main__":
    h = CANCommunicationHandler()
