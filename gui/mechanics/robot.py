import math
import yaml
import os
from typing import List, Tuple


class Robot:
    def __init__(self, *args, **kwargs) -> None:
        # Init variables
        self._lengths: tuple = (0.0, 0.0, 0.0, 0.0, 0.0)
        self._phi: List[float] = [0.0, 0.0, 0.0, 0.0]

        # End_points of arms
        self._r_m: List[float] = [25, 150]

        self._settings_file_path = self._get_settings_path()
        self._load_settings()
        
        # Overwrite the settings file if needed
        if "lengths" in kwargs:
            self.lengths = kwargs["lengths"]
        if "initial_position" in kwargs:
            self.r_m = kwargs["initial_position"]
        
        self._calculate_angles()

    def get_motor_angles(self, r_m: List[float]) -> Tuple[float, float]:
        """
        Calculate motor angles based on the given end point position

        Args:
            r_m (List[float]): End point of the robot

        Returns:
            Tuple[float, float]: Motor angles in radians
        """
        # Set the current end point
        self.r_m = r_m
        
        # Recalculate the robot position
        self._calculate_angles()
        return (self._phi[0], self._phi[1])

    
    def _load_settings(self) -> None:
        settings = None
        with open(self._settings_file_path, "r") as stream:
            try:
                settings = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        if settings:
            # Load lengths
            lengths_dict = settings["lengths"]
            order = ["l1", "l2", "l3", "l4", "l5"]
            self.lengths = tuple([lengths_dict[key] for key in order])
            
            # Load initial position
            initial_position_dict = settings["initial_position"]
            self.r_m = [initial_position_dict["x_m"], initial_position_dict["y_m"]]
            
            print(f"Settings loaded successfully")
            print(f"Lengths: {self.lengths}")
            print(f"initial position: {self.r_m}")

    def _calculate_angles(self):
        # Calculate angle phi_0 - see docu
        # TODO: add this to docu
        print("Recalculating angles")
        # Total length of end point from origin
        r_m_abs_2 = self.r_m[0] ** 2 + self.r_m[1] ** 2
        r_m_abs = math.sqrt(r_m_abs_2)
        phi_p12 = math.acos((r_m_abs_2) / (2 * self.l1 * r_m_abs))
        phi_p11 = math.atan2(self.r_m[1], self.r_m[0])
        phi_1 = phi_p11 + phi_p12
        phi_3 = math.atan2(
            self.r_m[1] - self.l1 * math.sin(phi_1),
            self.r_m[0] - self.l1 * math.cos(phi_1),
        )

        r_m_2 = (self.r_m[0] - self.l5, self.r_m[1])
        r_m_2_abs_2 = r_m_2[0] ** 2 + r_m_2[1] ** 2
        r_m_2_abs = math.sqrt(r_m_2_abs_2)
        phi_p21 = math.acos((r_m_2_abs_2) / (2 * self.l2 * r_m_2_abs))
        phi_p22 = math.atan2(r_m_2[1], r_m_2[0])
        phi_2 = phi_p22 - phi_p21

        phi_4 = math.atan2(
            r_m_2[1] - self.l2 *
            math.sin(phi_2), r_m_2[0] - self.l2 * math.cos(phi_2)
        )

        self.phi = [phi_1, phi_2, phi_3, phi_4]
        # [val/3.14*180 for val in self.phi]

    def _get_settings_path(self):
        current_dir = os.path.dirname(__file__)
        settings_path = os.path.join(current_dir, 'settings.yaml')
        return settings_path
    
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
        return self._lengths[2]

    @l2.setter
    def l2(self, value: float):
        self._lengths = (self.l1, value, self.l3, self.l4, self.l5)

    @property
    def l3(self) -> float:
        return self._lengths[3]

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
    from .drawer import Drawer
    robot = Robot()
    drawer = Drawer(robot)
    drawer.draw()
    r_m_0 = robot.r_m
