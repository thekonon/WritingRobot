import logging
import math
from typing import Tuple, List

from .mixins import RobotCalculationMixin
from ..logger import *
from ..constants import robotSettings


class Robot(RobotCalculationMixin):
    def __init__(self, 
                 lengths: Tuple[float, float, float, float, float]|None = None,
                 initial_position: Tuple[float, float]|None = None
                 ) -> None:
        self._setup_loger()
        self._setup_settings()
        if lengths:
            self.settings.LENGTHS = lengths
        if initial_position:
            self.settings.INIT_END_POINT = initial_position
        
        self._internal_angles: List[float] = [0, 0, 0, 0]
        self._r_m: List[float] = list(self.settings.INIT_END_POINT)
        
        self._recalculate()
        
    def set_motor_angles(self, 
                         angle_1: float|int|None,
                         angle_2: float|int|None
                         ) -> None:
        """
        Set wanted motor angles
        1) Calculates resulted end-point
        2) set_end_point is called
        3) Set to None if you want it unchanged
        """
        if not isinstance(angle_1, (int, float)) and angle_1 is not None:
            raise ValueError("First input argument must be float / int / None")
        if not isinstance(angle_2, (int, float)) and angle_2 is not None:
            raise ValueError("Second input argument must be float / int / None")
        
        if angle_1 is None:
            angle_1 = self._internal_angles[0]
        if angle_2 is None:
            angle_2 = self._internal_angles[2]
        
        self._r_m = self._calculate_end_point(angle_1, angle_2)
        self._recalculate()
        
    
    def get_motor_angles(self) -> Tuple[float, float]:
        """Return a tuple of motor angles"""
        return (self._internal_angles[0], self._internal_angles[2])
    
    def set_end_point(self, end_point: List[float]):
        """Set end -point of end efector, recalculate internal state"""
        if len(end_point) != 2:
            raise ValueError("Input must be 2 elements long")
        self.logger.info("Setting new end point")
        self._r_m = end_point
    
    def get_end_point(self) -> Tuple[float, float]:
        """Return a tuple of end - efector position"""
        return (self._r_m[0], self._r_m[1])
    
    def _recalculate(self):
        """Based on wanted end - point recalculate motor angles"""
        rm_abs = sum([i**2 for i in self._r_m])**0.5
        alfa = self.law_of_cosine_angle(self.settings.LENGTHS[1], self.settings.LENGTHS[0], rm_abs)
        beta = self.law_of_cosine_angle(self.settings.LENGTHS[0], self.settings.LENGTHS[1], rm_abs)
        gamma = self.atan2(self._r_m[1], self._r_m[0])
        phi1 = gamma + alfa
        phi2 = gamma - beta
        self.logger.debug(f"rm_abs: {rm_abs}")
        self.logger.debug(f"alfa: {alfa*180/3.14}")
        self.logger.debug(f"beta: {beta}")
        self.logger.debug(f"gamma: {gamma}")
        
        temp_rm = self._r_m
        temp_rm[0] -= self.settings.LENGTHS[4]
        rm_abs = sum([i**2 for i in temp_rm])**0.5
        alfa = self.law_of_cosine_angle(self.settings.LENGTHS[3], self.settings.LENGTHS[2], rm_abs)
        beta = self.law_of_cosine_angle(self.settings.LENGTHS[2], self.settings.LENGTHS[3], rm_abs)
        gamma = self.atan2(temp_rm[1], temp_rm[0])
        phi3 = gamma - alfa
        phi4 = gamma + beta
        
        self._internal_angles = [phi1, phi2, phi3, phi4]
        self._internal_angles = [angle if abs(angle)>0.05 else 0 for angle in self._internal_angles]
        self._internal_angles = [angle%6.28 for angle in self._internal_angles]
    
    def _calculate_end_point(self, angle_1: float, angle_2: float) -> List[float]:
        """Return end point of end efector based on provided motor angles"""
        return list(self.find_circle_intersections(
            self.settings.LENGTHS[0]*math.cos(angle_1),
            self.settings.LENGTHS[0]*math.sin(angle_1),
            self.settings.LENGTHS[1],
            self.settings.LENGTHS[2]*math.cos(angle_2) + self.settings.LENGTHS[4],
            self.settings.LENGTHS[2]*math.sin(angle_2),
            self.settings.LENGTHS[3]))
    
    def _setup_settings(self):
        self.logger.log(logging.INFO, "Getting robot settings")
        self.settings: robotSettings = robotSettings()
        msg = """Settings:
                l1: {} 
                l2: {}
                l3: {}
                l4: {}
                l5: {}""".format(*self.settings.LENGTHS)
        self.logger.log(logging.INFO, msg)
    
    def _setup_loger(self):
        self.logger = logging.getLogger("Robot")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(get_logger_console_handler())
        self.logger.addHandler(get_logger_file_handler())
        # self.logger.log(logging.ERROR, "FAILED")
        self.logger.log(logging.INFO, "Robot initialization started")