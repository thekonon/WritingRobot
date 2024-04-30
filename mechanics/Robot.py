import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Tuple


class Robot:
    def __init__(
        self,
        lengths: tuple = (
            100.0,
            100.0,
            100.0,
            100.0,
            50.0,
        ),
    ) -> None:
        # Lengths of arms, l = (l1, l2, l3, l4), they're constant
        self._lengths = (0.0, 0.0, 0.0, 0.0, 0.0)
        # End_points of arms
        self._r_m: List[float] = [25, 150]
        # Init angles
        self._phi = [0.0, 0.0, 0.0, 0.0]

        # Set lengths
        self.lengths = lengths

        self._calculate_angles()

    def _calculate_angles(self):
        # Calculate angle phi_0 - see docu
        # TODO: add this to docu
        print("recalculating angles")
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
            r_m_2[1] - self.l2 * math.sin(phi_2), r_m_2[0] - self.l2 * math.cos(phi_2)
        )

        self.phi = [phi_1, phi_2, phi_3, phi_4]
        # [val/3.14*180 for val in self.phi]

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


class Drawer:
    def __init__(self, robot: Robot):
        self.robot: Robot = robot
        self._init_matplotlib()

    def draw(self):
        self.ax.clear()  # Clear the previous plot
        # Left part
        end_point_1 = self._draw_line((0, 0), self.robot.phi_1, self.robot.l1)
        end_point_3 = self._draw_line(end_point_1, self.robot.phi_3, self.robot.l3)
        if end_point_1[1] < 0:
            pass

        # Right part
        end_point_2 = self._draw_line(
            (self.robot.l5, 0), self.robot.phi_2, self.robot.l2
        )
        end_point_4 = self._draw_line(end_point_2, self.robot.phi_4, self.robot.l4)

        self._set_ax_limits()

        plt.draw()  # Update the plot

    def _init_matplotlib(self):
        self.fig, self.ax = plt.subplots()
        self._set_ax_limits()

    def _set_ax_limits(self):
        self.ax.set_xlim(-150, 150)
        self.ax.set_ylim(-50, 250)

    def _draw_line(self, start_point: tuple, phi: float, length: float) -> tuple:
        end_point = (
            start_point[0] + length * math.cos(phi),
            start_point[1] + length * math.sin(phi),
        )
        self._plot_line(start_point, end_point)
        return end_point

    def _plot_line(self, start_point: tuple, end_point: tuple):
        self.ax.plot(
            (start_point[0], end_point[0], end_point[0]),
            (start_point[1], end_point[1], end_point[1]),
            label="Left Arm",
            color="red",
            linewidth=2,
            linestyle="-",
        )


if __name__ == "__main__":
    robot = Robot()
    drawer = Drawer(robot)
    drawer.draw()
    r_m_0 = robot.r_m

    robot.x_m = 30
    # w = 0.1
    # for t in range(300):
    #     robot.r_m = [r_m_0[0] + 30*math.sin(w*t), r_m_0[1] + 30*math.cos(w*t)]
    #     robot._calculate_angles()
    #     plt.pause(0.01)
    #     drawer.draw()
