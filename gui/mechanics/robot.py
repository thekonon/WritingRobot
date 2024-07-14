import math
import yaml
import os
import gui.constants as constants
import logging
from gui._logger_settings import get_logger_console_handler, get_logger_file_handler
from typing import List, Tuple
from abc import ABC, abstractmethod, abstractproperty

class RobotInterface(ABC):
    @abstractmethod
    def get_motor_angles(self) -> List[float]:
        pass
    
    @abstractmethod
    def set_phi_1(self) -> None:
        pass
    
    @abstractmethod
    def set_phi_2(self) -> None:
        pass
    
    @abstractproperty
    def r_m(self):
        pass
    
class Robot(RobotInterface):
    def __init__(self, *args, **kwargs) -> None:
        self._setup_loger()
        self.logger.info("Robot initialization started")
        
        self._load_parameters()
        if kwargs:
            self._handle_arguments(kwargs)
        
        self._calculate_angles()
                

    def get_motor_angles(self, r_m: List[float]|None = None, output_in_degrees = False) -> Tuple[float, float]:
        if r_m:
            self.r_m = r_m
        return (self.phi_1, self.phi_3)

    def set_phi_1(self, phi_1: float) -> None:
        pass

    def set_phi_2(self, phi_2: float) -> None:
        pass
    
    def _calculate_angles(self):
        """
        This function updates all angles based on robot lengths and end point
        """
        self.logger.info("Recalculating the angles")

        # ____________________________________________ #
        # Left part of robot
        r_m_2       = self.r_m[0]**2 + self.r_m[1]**2
        r_m_abs     = r_m_2**0.5
        if r_m_abs == 0 and (self.l1 != 0 or self.l2 != 0):
            self.logger.error("Endpoint is unreachable with given arm lengths")
            raise ValueError("Endpoint is unreachable with given arm lengths")
        # Case with zero lengths and zero end point
        if r_m_abs == 0 and sum(self.lengths) == 0:
            return [0,0,0,0]
        if r_m_abs > (self.l1+self.l2):
            self.logger.error("First arm got out of range")
            raise ValueError("First arm is out of reach")
        
        phi_0       = math.acos((- self.l1**2 + self.l2**2 + r_m_2) / (2*self.l2*r_m_abs))
        tilde_phi_1 = math.acos((+ self.l1**2 - self.l2**2 + r_m_2) / (2*self.l1*r_m_abs))
        phi_RM      = math.atan2(self.r_m[1], self.r_m[0])
        if phi_RM < 0:
            phi_RM += 2*math.pi
        phi_1       = tilde_phi_1 + phi_RM
        l2_vec      =   ( 
                        self.r_m[0] - self.l1*math.cos(phi_1),
                        self.r_m[1] - self.l1*math.sin(phi_1)
                        )
        phi_2       = math.atan2(l2_vec[1], l2_vec[0])
        if phi_2 < 0:
            phi_2+=2*math.pi # put phy_2 in range 0 - 2*pi
        
        # ____________________________________________ #
        # Right part of robot
        r_m_2       = (self.r_m[0]-self.l5)**2 + self.r_m[1]**2
        r_m_abs     = r_m_2**0.5
        if r_m_abs > (self.l3+self.l4):
            self.logger.error("Second arm got out of range")
            raise ValueError("Second arm is out of reach")
        phi_0       = math.acos((- self.l3**2 + self.l4**2 + r_m_2) / (2*self.l4*r_m_abs))
        phi_RM      = math.atan2(self.r_m[1], (self.r_m[0]-self.l5))
        if phi_RM < 0:
            phi_RM+=2*math.pi
        tilde_phi_3 = math.acos((+ self.l3**2 - self.l4**2 + r_m_2) / (2*self.l3*r_m_abs))
        phi_3       = phi_RM - tilde_phi_3
        l4_vec      =   ( 
                        self.r_m[0] - self.l3*math.cos(phi_3) - self.l5,
                        self.r_m[1] - self.l3*math.sin(phi_3)
                        )
        phi_4       = math.atan2(l4_vec[1], l4_vec[0])
        if phi_4 < 0:
            phi_4+=2*math.pi
        
        
        self._phi = [phi_1, phi_2, phi_3, phi_4]
        self._phi = [phi%(2*math.pi) for phi in self._phi]
        self.logger.info(f"Angles: {self._phi}")
        
    def print_current_state(self) -> None:
        pass
    
    def _load_parameters(self):
        # Load default parameters
        self.logger.info("Setting up default parameters")
        self._lengths: tuple    = constants.Robot.LENGTHS
        self._r_m: List[float]  = constants.Robot.INIT_END_POINT
        self._phi: List[float] = [0.0, 0.0, 0.0, 0.0]
        
    def _setup_loger(self):
        self.logger = logging.getLogger("Robot")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(get_logger_console_handler())
        self.logger.addHandler(get_logger_file_handler())
        
    def _handle_arguments(self, kwargs):
        # Overwrite the settings file if needed
        self.logger.info("Input arguments found, overwriting robot settings")
        possible_overwrites = \
            {
                "lengths":              "lengths",
                "initial_position":     "_r_m"  #setting internal variable
            }
        for value, key in possible_overwrites.items():
            if value in kwargs:
                self.logger.info(f"Overwriting variable {key} with value {kwargs[value]}")
                setattr(self, key, kwargs[value])
        
        
    def __iadd__(self, values: List[float]):
        pass

    def __isub__(self, values: List[float]):
        pass

    @property
    def r_m(self) -> List[float]:
        """Return end point"""
        return self._r_m

    @r_m.setter
    def r_m(self, value: List[float]):
        """Set the end point + recalculates angle"""
        if len(value) != 2:
            raise ValueError("r_m must be a list of 2 elements")
        self._r_m = value
        self._calculate_angles()

    @property
    def x_m(self) -> float:
        return self.r_m[0]

    @x_m.setter
    def x_m(self, value: float):
        self.r_m = [self.r_m[0] + value, self.r_m[1]]

    @property
    def y_m(self) -> float:
        return self.r_m[1]

    @y_m.setter
    def y_m(self, value: float):
        self.r_m = [self.r_m[0], self.r_m[1] + value]

    @property
    def phi(self) -> List[float]:
        return self._phi

    @phi.setter
    def phi(self, value: List[float]):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_1(self) -> float:
        return self._phi[0]

    @phi_1.setter
    def phi_1(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_2(self) -> float:
        return self._phi[1]

    @phi_2.setter
    def phi_2(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_3(self) -> float:
        return self._phi[2]

    @phi_3.setter
    def phi_3(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_4(self) -> float:
        return self._phi[3]

    @phi_4.setter
    def phi_4(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def lengths(self) -> tuple:
        return self._lengths

    @lengths.setter
    def lengths(self, value: tuple):
        if len(value) == 5:
            self._lengths = value
        else:
            raise ValueError("Length of value have to be 5")

    @property
    def l1(self) -> float:
        return self._lengths[0]

    @l1.setter
    def l1(self, value: float):
        self._lengths = (value, self.l2, self.l3, self.l4, self.l5)

    @property
    def l2(self) -> float:
        return self._lengths[1]

    @l2.setter
    def l2(self, value: float):
        self._lengths = (self.l1, value, self.l3, self.l4, self.l5)

    @property
    def l3(self) -> float:
        return self._lengths[2]

    @l3.setter
    def l3(self, value: float):
        self._lengths = (self.l1, self.l2, value, self.l4, self.l5)

    @property
    def l4(self) -> float:
        return self._lengths[3]

    @l4.setter
    def l4(self, value: float):
        self._lengths = (self.l1, self.l2, self.l3, value, self.l5)

    @property
    def l5(self) -> float:
        return self._lengths[4]

    @l5.setter
    def l5(self, value: float):
        self._lengths = (self.l1, self.l2, self.l3, self.l4, value)
        


if __name__ == "__main__":
    robot = Robot()
