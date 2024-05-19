# from . import Robot
import math
from matplotlib import pyplot as plt
class Drawer:
    def __init__(self, robot):
        self.robot = robot
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