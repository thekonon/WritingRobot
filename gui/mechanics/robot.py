import math
from multiprocessing.sharedctypes import Value
import yaml
import os
import gui.constants as constants
import logging
from .robot_mixins import RobotInterface
from .._logger_settings import get_logger_console_handler, get_logger_file_handler
from typing import List, Tuple
from abc import ABC, abstractmethod, abstractproperty


class Robot(RobotInterface):
    def __init__(self, *args, **kwargs) -> None:
        self._setup_loger()
        self.logger.info("Robot initialization started")
        
        # Load default parameters
        self._load_parameters()
        
        # If extra parameters are in kwargs - overwrite default
        if kwargs:
            self._handle_arguments(kwargs)
        
        self._calculate_angles()
                

    def get_motor_angles(self, r_m: List[float]|None = None, output_in_degrees = False) -> Tuple[float, float]:
        """Return angles of motor 1 and motor 2"""
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
        if not self.check_if_point_is_in_both_circles(self.r_m, self.l1+self.l2, self.l3+self.l4, self.l5):
            raise ValueError("Robot has not reach to that point")

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
        
        phi_0       = self.law_of_cosine_angle(self.l1, self.l2, r_m_abs)
        tilde_phi_1 = self.law_of_cosine_angle(self.l2, self.l1, r_m_abs)
        phi_RM      = self.atan2(self.r_m[1], self.r_m[0])
        phi_1       = tilde_phi_1 + phi_RM
        l2_vec      =   (   self.r_m[0] - self.l1*math.cos(phi_1),
                            self.r_m[1] - self.l1*math.sin(phi_1))
        phi_2       = self.atan2(l2_vec[1], l2_vec[0])
        
        # ____________________________________________ #
        # Right part of robot
        r_m_2       = (self.r_m[0]-self.l5)**2 + self.r_m[1]**2
        r_m_abs     = r_m_2**0.5
        phi_0       = self.law_of_cosine_angle(self.l3, self.l4, r_m_abs)
        tilde_phi_3 = self.law_of_cosine_angle(self.l4, self.l3, r_m_abs)
        phi_RM      = self.atan2(self.r_m[1], (self.r_m[0]-self.l5))
        
        phi_3       = phi_RM - tilde_phi_3
        l4_vec      =   (   self.r_m[0] - self.l3*math.cos(phi_3) - self.l5,
                            self.r_m[1] - self.l3*math.sin(phi_3))
        phi_4       = self.atan2(l4_vec[1], l4_vec[0])
        
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


if __name__ == "__main__":
    robot = Robot()
