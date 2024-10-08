import can
import os
from typing import List, Any, Literal
from enum import Enum


class BitRates(Enum):
    """Enum class to store CAN bus bit rates.

    Attributes:
        _125KHZ (int): CAN bus bit rate of 125000 bits per second.
    """

    #: CAN bus bit rate of 125000 bits per second.
    _125KHZ = 125000
    """The value of the CAN bus bit rate of 125000 bits per second."""


class CANCommunicationHandler:
    """# CANCOmmunicationHandler
    1) Create this object
    2) Modify data
        a) obj.motor_data_frame.set_data(data)
    3) Send data via CAN BUS
    """

    def __init__(self) -> None:

        self.bus: can.BusABC

        # Communicatino settings
        self._BITRATE: int = BitRates._125KHZ.value
        self._CAN_INTERFACE: str = "can0"
        self._BUS_TYPE: str = "socketcan"

        # MotorDataFrame settings
        self.motor_data_frame: MotorDataFrame = MotorDataFrame()

        # State variables
        self._init_done: int = 0

    def send_data(self, selected_type: str) -> None:
        """Send all frames via can"""
        if not self._init_done:
            raise ValueError("Initialization needs to be done")
        types = {"MotorDataFrame": self.motor_data_frame.get_msg()}
        msg = types.get(selected_type)
        if msg:
            print("Sending msg!")
            self.bus.send(msg)
        else:
            raise ValueError("Uknown type message selected")

    def init_communication(self) -> Any:
        if os.name == "nt":
            raise NotImplementedError("Implementation for Windows not implemented")
        os.system("sudo ip link set can0 up type can bitrate 125000")
        # os.system("sudo ip link set can0 up")
        self.bus = can.interface.Bus(
            channel=self._CAN_INTERFACE, bustype=self._BUS_TYPE
        )
        self._init_done = 1

    def end_communication(self) -> None:
        if not self._init_done:
            return None
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

    def set_data(self, data: List[int], motor: int = 0) -> None:
        if motor:
            self.data[:4] = data
        else:
            self.data[4:] = data
        self._create_msg()

    def get_msg(self) -> can.Message:
        return self._msg

    def _create_msg(self) -> None:
        self._msg: can.Message = can.Message(
            arbitration_id=self.MSG_ID, is_extended_id=False, data=self.data
        )


if __name__ == "__main__":
    h: CANCommunicationHandler = CANCommunicationHandler()
