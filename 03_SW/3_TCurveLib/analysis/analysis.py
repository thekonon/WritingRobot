import tkinter as tk
import tcurve
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Any, Tuple

curve = tcurve.TCurve()

error, position = curve.get_point(0.5)


class CurvePlotter:

    def __init__(self, a_max: float = 10, w_max: float = 5, dp: float = 1) -> None:
        self._total_points_to_display = 100
        self.curve = tcurve.TCurve()
        self.setCurve(a_max, w_max, dp)

        self.fig, self.ax = plt.subplots()
        (self.line,) = self.ax.plot([], [])

        self.ax.set_xlabel("t")
        self.ax.set_ylabel("q")
        self.ax.set_title("Curve")
        self.ax.grid(True)

    def setCurve(self, a_max: float, w_max: float, dp: float):
        self.curve.set_acceleration(a_max)
        self.curve.set_max_velocity(w_max)
        self.curve.set_delta_phi(dp)

    def update(self):
        times, data = self._get_data()
        values = data[:, 1]

        self.line.set_data(times, values)

        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def show(self):
        plt.ion()  # interactive mode
        self.update()
        plt.show()

    def _get_times(self) -> np.ndarray[Any, Any]:
        return np.linspace(0, self.curve.get_tmax(), self._total_points_to_display)

    def _get_data(self) -> Tuple[np.ndarray[Any, Any], np.ndarray[Any, Any]]:
        times = self._get_times()
        return times, np.array([self.curve.get_point(ti) for ti in times])


if __name__ == "__main__":
    plotter = CurvePlotter()

    plotter.show()


    
    while True:
        res = input("a, w, dp: ")
        res = res.split(",")
        res = [float(res_i) for res_i in res]
        plotter.setCurve(*res)
        plotter.update()

        plt.show(block=False)
            
        
