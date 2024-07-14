from abc import ABC, abstractmethod, abstractproperty
from typing import List
import math

class RobotCalculationMixin:
    @staticmethod
    def law_of_cosine_angle(a, b, c) -> float:
        """Return angle oposing side A (alfa angle in radians)"""
        if a < 0 or b < 0 or c < 0:
            raise ValueError("All numbers must be possitive")
        if (a+b) < c or (a+c) < b or (b+c) < a:
            raise ValueError("Triangle unequality is not met")
        return math.acos((b**2+c**2-a**2)/(2*b*c))
    
    @staticmethod
    def atan2(y, x) -> float:
        if x == 0 and y == 0:
            raise ValueError("Both x and y can not be 0 for arctan function")
        angle = math.atan2(y, x)
        if angle < 0:
            angle += 2*math.pi
        return angle
    
    @staticmethod
    def check_if_point_is_in_both_circles(point: tuple|list, r1: float, r2: float, l5: float) -> bool:
        def _calculate_distance_between_points(point1: tuple|list, point2: tuple|list) -> float:
            dx = point1[0] - point2[0]
            dy = point1[1] - point2[1]
            return (dx**2+dy**2)**0.5
        distance_to_first_point = _calculate_distance_between_points(point, (0, 0))
        distance_to_second_point = _calculate_distance_between_points(point, (l5, 0))
        if distance_to_first_point <= r1 and distance_to_second_point <= r2:
            return True
        return False
    
    
    

class RobotPropertiesMixin:
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
        self._calculate_angles() # type: ignore

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
        return self._phi # type: ignore

    @phi.setter
    def phi(self, value: List[float]):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_1(self) -> float:
        return self._phi[0] # type: ignore

    @phi_1.setter
    def phi_1(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_2(self) -> float:
        return self._phi[1] # type: ignore

    @phi_2.setter
    def phi_2(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_3(self) -> float:
        return self._phi[2] # type: ignore

    @phi_3.setter
    def phi_3(self, value: float):
        raise PermissionError("Phi can no be set like using obj.phi")

    @property
    def phi_4(self) -> float:
        return self._phi[3] # type: ignore

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

class RobotInterface(ABC, RobotPropertiesMixin, RobotCalculationMixin):
    @abstractmethod
    def get_motor_angles(self) -> List[float]:
        pass
    
    @abstractmethod
    def set_phi_1(self) -> None:
        pass
    
    @abstractmethod
    def set_phi_2(self) -> None:
        pass