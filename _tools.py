import can
import os
from typing import List
from enum import Enum
from can import Message

class CANCommunicationHandler:
    """CAN communication handler for motor control.

    Args:
        bitrate (int): CAN bus bitrate.
        interface (str): CAN bus interface.
        bustype (str): CAN bus type.
    """
    def __init__(self, bitrate: int = 125000, interface: str = 'can0', bustype: str = 'socketcan') -> None:
        self.bus = can.Bus()
        self.bitrate = bitrate
        self.interface = interface
        self.bustype = bustype
        self.motor_data_frame = MotorDataFrame()
        self.communication_initialized = False

    def send_data(self, frame_type: str) -> None:
        """Send CAN frame.

        Args:
            frame_type (str): Type of frame to send.
        Raises:
            ValueError: If communication is not initialized.
            ValueError: If unknown frame type selected.
        """
        if not self.communication_initialized:
            raise ValueError("Initialization needs to be done")
        frames = {"MotorDataFrame": self.motor_data_frame.get_msg()}
        frame = frames.get(frame_type)
        if frame:
            self.bus.send(frame)
        else:
            raise ValueError('Unknown frame type selected')

    def initialize_communication(self) -> None:
        """Initialize CAN communication.

        Raises:
            NotImplementedError: If implementation for Windows not implemented.
        """
        if os.name == 'nt':
            raise NotImplementedError('Implementation for Windows not implemented')
        os.system(f"sudo ip link set {self.interface} up type can bitrate {self.bitrate}")
        self.bus = can.interface.Bus(channel=self.interface, bustype=self.bustype)
        self.communication_initialized = True

    def finalize_communication(self) -> None:
        """Finalize CAN communication."""
        self.bus.shutdown()
        os.system(f"sudo ip link set {self.interface} down")


class MotorDataFrame:
    """MotorDataFrame class for motor control.

    Args:
        total_motors (int): Number of motors to be controlled.
    """
    def __init__(self, total_motors: int = 1) -> None:
        """
        Initialize MotorDataFrame.

        Args:
            total_motors (int): Number of motors to be controlled.
        """
        self.total_motors: int = total_motors
        self.MSG_ID: int = 0
        self._msg_length: int = 4 if self.total_motors == 1 else 8
        self.data: List[int] = [0] * self._msg_length
        self._create_msg()
    
    def set_data(self, data: List[int], motor: int = 0) -> None:
        """
        Set data for motor.

        Args:
            data (List[int]): Data for motor.
            motor (int): Motor number.
        """
        if motor:
            self.data[:4] = data
        else:
            self.data[4:] = data
        self._create_msg()
    
    def get_msg(self) -> Message:
        """Get can.Message object.

        Returns:
            can.Message: CAN message.
        """
        return self._msg
        
    def _create_msg(self) -> None:
        """Create can.Message object.
        """
        self._msg = Message(\
            arbitration_id = self.MSG_ID,
            is_extended_id = False,
            data = self.data
        )
    

if __name__ == "__main__":
    h = CANCommunicationHandler()
