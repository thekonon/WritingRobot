import math
import yaml
import os
import gui.constants as constants
from typing import List, Tuple
from abc import ABC, abstractmethod

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
    
class Robot(RobotInterface):
    """
        # Class for computing the movements
        
        ## Initialization - parameters:
        
        ### lengths:
        e.g. lengths = (100, 100, 100, 100, 50) \n
        Set the lengths of arms of the Robot
        
        ### initial_position: 
        e.g. initial_position = [50, 150] \n
        Set the initial end point of arms
        
        ## Avaiable methods:
        
        get_motor_angles() -> List[float] \n
        return a list of all angles of Robot
        
        ## Avaible operations:
        
        ### Robot +- tuple
        
        Change end point by substracting a list
    """
    
    def __init__(self, *args, **kwargs) -> None:
        print("Robot initialization started")
        
        # Init variables
        self._lengths: tuple = constants.Robot.LENGTHS

        # End_points of arms
        self._r_m: List[float] = constants.Robot.INIT_END_POINT

        # Overwrite the settings file if needed
        # expected in kwargs - saved as in self.(value)
        possible_overwrites = \
            {
                "lengths":              "lengths",
                "initial_position":     "r_m"
            }
        for value, key in possible_overwrites.items():
            if value in kwargs:
                print(f"Overwriting variable {key} with value {kwargs[value]}")
                setattr(self, key, kwargs[value])
                
        print("-"*60)
        print("Robot initialized with following parameters: ")
        print(f"Lengths: {self._lengths}")
        print(f"Init point: {self._r_m}")
        print("-"*60)
        
        print("Calculating initial angles")
        self._phi: List[float] = [0.0, 0.0, 0.0, 0.0]
        self._calculate_angles()
        print("Successfully done")
        print("-"*60)

    def get_motor_angles(self, r_m: List[float]|None = None, output_in_degrees = False) -> Tuple[float, float]:
        """
        Calculate motor angles based on the given end point position

        Args:
            r_m (List[float])| None: End point of the robot

        Returns:
            Tuple[float, float]: Motor angles in radians (possibility in degree)
        """
        if r_m:
            # Set the current end point
            self.r_m = r_m

            # Recalculate the robot position
            self._calculate_angles()
        if output_in_degrees:
            return (self._phi[0]/math.pi*180, self._phi[1]/math.pi*180)    
        return (self._phi[0], self._phi[1])

    def set_phi_1(self, phi_1: float) -> None:
        self.phi_1 = phi_1
        A: tuple = (self.l1 * math.cos(self.phi_1), self.l1 * math.sin(self.phi_1))
        B: tuple = (self.l5 + self.l2 * math.cos(self.phi_2), self.l2 * math.sin(self.phi_2))
        AB: tuple = (B[0] - A[0], B[1] - A[1])
        AB_2: float   = AB[0] ** 2 + AB[1] ** 2
        alfa_0: float = math.atan2(AB[1], AB[0])
        alfa_1: float = math.acos(AB_2/(2*self.l3*math.sqrt(AB_2)))
        self.phi_3 = alfa_0+alfa_1
        self.phi_4 = math.pi+alfa_0-alfa_1
        
    def set_phi_2(self, phi_2: float) -> None:
        self.phi_2 = phi_2
        A: tuple = (self.l1 * math.cos(self.phi_1), self.l1 * math.sin(self.phi_1))
        B: tuple = (self.l5 + self.l2 * math.cos(self.phi_2), self.l2 * math.sin(self.phi_2))
        AB: tuple = (B[0] - A[0], B[1] - A[1])
        AB_2: float   = AB[0] ** 2 + AB[1] ** 2
        alfa_0: float = math.atan2(AB[1], AB[0])
        alfa_1: float = math.acos(AB_2/(2*self.l3*math.sqrt(AB_2)))
        self.phi_3 = alfa_0+alfa_1
        self.phi_4 = math.pi+alfa_0-alfa_1

    def _calculate_angles(self):
        # Calculate angle phi_0 - see docu
        # TODO: add this to docu
        # print("Recalculating angles")
        # Total length of end point from origin
        r_m_abs_2 = self.r_m[0] ** 2 + self.r_m[1] ** 2
        r_m_abs = math.sqrt(r_m_abs_2)
        phi_p12 = math.acos((-self.l3**2+self.l1**2+r_m_abs_2) / (2 * self.l1 * r_m_abs))
        phi_p11 = math.atan2(self.r_m[1], self.r_m[0])
        phi_1 = phi_p11 + phi_p12
        phi_3 = math.atan2(
            self.r_m[1] - self.l1 * math.sin(phi_1),
            self.r_m[0] - self.l1 * math.cos(phi_1),
        )

        r_m_2 = (self.r_m[0] - self.l5, self.r_m[1])
        r_m_2_abs_2 = r_m_2[0] ** 2 + r_m_2[1] ** 2
        r_m_2_abs = math.sqrt(r_m_2_abs_2)
        phi_p21 = math.acos((-self.l4**2+self.l2**2+r_m_2_abs_2) / (2 * self.l2 * r_m_2_abs))
        phi_p22 = math.atan2(r_m_2[1], r_m_2[0])
        phi_2 = phi_p22 - phi_p21

        phi_4 = math.atan2(
            r_m_2[1] - self.l2 *
            math.sin(phi_2), r_m_2[0] - self.l2 * math.cos(phi_2)
        )

        self.phi = [phi_1, phi_2, phi_3, phi_4]
        # [val/3.14*180 for val in self.phi]

    def print_current_state(self) -> None:
        print("-"*60)
        print("Printing current state: ")
        print(f"Lengths: {self._lengths}")
        for idx, phi in enumerate(self._phi):
            print(f"Phi{idx+1}: {phi:.3f} rad | {phi/3.14*180:.3f} deg")

    @property
    def r_m(self) -> List[float]:
        return self._r_m

    @r_m.setter
    def r_m(self, value: List[float]):
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
        if len(value) != 4:
            raise ValueError("phi must be a list of 4 elements")
        self._phi = value

    @property
    def phi_1(self) -> float:
        return self._phi[0]

    @phi_1.setter
    def phi_1(self, value: float):
        self._phi[0] = value

    @property
    def phi_2(self) -> float:
        return self._phi[1]

    @phi_2.setter
    def phi_2(self, value: float):
        self._phi[1] = value

    @property
    def phi_3(self) -> float:
        return self._phi[2]

    @phi_3.setter
    def phi_3(self, value: float):
        self._phi[2] = value

    @property
    def phi_4(self) -> float:
        return self._phi[3]

    @phi_4.setter
    def phi_4(self, value: float):
        self._phi[3] = value

    @property
    def lengths(self) -> tuple:
        return self._lengths

    @lengths.setter
    def lengths(self, value: tuple):
        if len(value) == 5:
            self._lengths = value
        else:
            raise ValueError("Length of value should be 5")

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
        
    def __iadd__(self, values: List[float]):
        if len(values) != len(self._r_m):
            raise ValueError("Length of values must match length of r_m")
        self._r_m = [a + b for a, b in zip(self._r_m, values)]
        self._calculate_angles()
        return self

    def __isub__(self, values: List[float]):
        if len(values) != len(self._r_m):
            raise ValueError("Length of values must match length of r_m")
        self._r_m = [a - b for a, b in zip(self._r_m, values)]
        self._calculate_angles()
        return self


if __name__ == "__main__":
    from .drawer import Drawer
    robot = Robot()
    drawer = Drawer(robot)
    drawer.draw()
    r_m_0 = robot.r_m
