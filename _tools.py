import can
import os
from typing import List
from enum import Enum

class CANCommunicationHandler:
    """CAN communication handler for motor control."""
    def __init__(self, bitrate: int = 125000, interface: str = 'can0', bustype: str = 'socketcan'):
        self.bus = can.Bus()
        self.bitrate = bitrate
        self.interface = interface
        self.bustype = bustype
        self.motor_data_frame = MotorDataFrame()
        self.communication_initialized = False

    def send_data(self, frame_type: str):
        if not self.communication_initialized:
            raise ValueError("Initialization needs to be done")
        frames = {"MotorDataFrame": self.motor_data_frame.get_msg()}
        frame = frames.get(frame_type)
        if frame:
            self.bus.send(frame)
        else:
            raise ValueError('Unknown frame type selected')

    def initialize_communication(self):
        if os.name == 'nt':
            raise NotImplementedError('Implementation for Windows not implemented')
        os.system(f"sudo ip link set {self.interface} up type can bitrate {self.bitrate}")
        self.bus = can.interface.Bus(channel=self.interface, bustype=self.bustype)
        self.communication_initialized = True

    def finalize_communication(self):
        self.bus.shutdown()
        os.system(f"sudo ip link set {self.interface} down")
        
        
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
        self._msg = can.Message(\
            arbitration_id = self.MSG_ID,
            is_extended_id = False,
            data = self.data
        )
    

if __name__ == "__main__":
    h = CANCommunicationHandler()