import logging
import math
from typing import Tuple, List

from .mixins import RobotCalculationMixin
from .circle import Circle
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
        self._recalculate()
    
    def get_end_point(self) -> Tuple[float, float]:
        """Return a tuple of end - efector position"""
        return (self._r_m[0], self._r_m[1])
    
    def get_points(self) -> tuple:
        point_0: tuple = (0, 0)
        point_1: tuple = (self.settings.LENGTHS[0] * math.cos(self._internal_angles[0]),
                          self.settings.LENGTHS[0] * math.sin(self._internal_angles[0]))
        point_2: tuple = (point_1[0] + self.settings.LENGTHS[1] * math.cos(self._internal_angles[1]),
                          point_1[1] + self.settings.LENGTHS[1] * math.sin(self._internal_angles[1]))
        point_3: tuple = (self.settings.LENGTHS[4],
                          0)
        point_4: tuple = (point_3[0] + self.settings.LENGTHS[2]* math.cos(self._internal_angles[2]), 
                          point_3[1] + self.settings.LENGTHS[2]* math.sin(self._internal_angles[2]))
        point_5: tuple = (point_4[0] + self.settings.LENGTHS[3]* math.cos(self._internal_angles[3]), 
                          point_4[1] + self.settings.LENGTHS[3]* math.sin(self._internal_angles[3]))
        error: float = (point_2[0]-point_5[0])**2+(point_2[1]-point_5[1])**2
        if error > 1e-8:
            self.logger.warning(f"error is {error}") 
        return (point_0, point_1, point_2, point_3, point_4, point_5)
    
    def get_limits(self) -> list:
        points = []
        for i in range(628):
            angle: float = i/100    
            mid_point_circle_1: tuple = (self.settings.LENGTHS[0] * math.cos(angle),
                                        self.settings.LENGTHS[0] * math.sin(angle))
            circle_1: Circle = Circle(mid_point_circle_1, self.settings.LENGTHS[1] +self.settings.LENGTHS[3])
            mid_point_circle_2: tuple = (self.settings.LENGTHS[4],
                                        0)
            circle_2: Circle = Circle(mid_point_circle_2, self.settings.LENGTHS[2])
            try:
                intersections = circle_1.intersection(circle_2)
                point_of_interest = intersections[1]
                if intersections[0][1] > intersections[1][1]:
                    point_of_interest = intersections[0]
                
                points.append(((mid_point_circle_1[0]+point_of_interest[0])/2, (mid_point_circle_1[1]+point_of_interest[1])/2))
            except ValueError as ex:
                pass

        return points
    
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