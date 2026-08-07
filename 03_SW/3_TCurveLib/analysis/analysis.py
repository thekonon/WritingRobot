import tcurve
import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Tuple
from tkinter import ttk
import tkinter as tk

curve = tcurve.TCurve()

error, position = curve.get_point(0.5)


class CurvePlotter:

    def __init__(self, a_max: float = 10, w_max: float = 5, dp: float = 1) -> None:
        self._points_count = 100
        self.curve = tcurve.TCurve()
        self.setCurve(a_max, w_max, dp)

        self.fig, self.ax = plt.subplots()
        (self.position_line,) = self.ax.plot([], [], label="Position")
        (self.velocity_line,) = self.ax.plot([], [], label="Velocity")
        (self.acceleration_line,) = self.ax.plot([], [], label="Acceleration")

        self.ax.legend()

        self.ax.set_xlabel("t")
        self.ax.set_ylabel("q")
        self.ax.set_title("Curve")
        self.ax.grid(True)

    def setCurve(self, a_max: float, w_max: float, dp: float):
        self.curve.set_acceleration(a_max)
        self.curve.set_max_velocity(w_max)
        self.curve.set_delta_phi(dp)
    def update(self):
        times, position = self._get_data()
        _, velocity, acceleration = self._get_derivatives()

        self.position_line.set_data(times, position)
        self.velocity_line.set_data(times, velocity)
        self.acceleration_line.set_data(times, acceleration)

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()

    def show(self):
        plt.ion()  # interactive mode
        self.update()
        plt.show()

    def _get_times(self) -> np.ndarray[int, Any]:
        return np.linspace(0, self.curve.get_tmax(), self._points_count)

    def _get_data(self) -> Tuple[np.ndarray[Any, Any], np.ndarray[Any, Any]]:
        times = self._get_times()
        return times, np.array([self.curve.get_point(ti)[1] for ti in times])
    
    def _get_derivatives(self) -> Tuple[np.ndarray[Any, Any], np.ndarray[Any, Any], np.ndarray[Any, Any]]:
        times, data = self._get_data()
        dt = np.diff(times, prepend=times[0])
        derivative = np.gradient(data[:], times)
        acceleration = np.gradient(derivative[:], times)
        return dt, derivative, acceleration


class CurveController:
    def __init__(self, plotter: CurvePlotter):
        self.plotter = plotter

        self.root = tk.Tk()
        self.root.title("TCurve Controller")

        # Variables
        self.a_var = tk.DoubleVar(value=10.0)
        self.w_var = tk.DoubleVar(value=5.0)
        self.dp_var = tk.DoubleVar(value=1.0)

        self._create_slider(
            "Max acceleration",
            self.a_var,
            0.1,
            50.0,
            0,
        )

        self._create_slider(
            "Max velocity",
            self.w_var,
            0.1,
            20.0,
            1,
        )

        self._create_slider(
            "Delta phi",
            self.dp_var,
            0.01,
            20.0,
            2,
        )

        ttk.Button(
            self.root,
            text="Update",
            command=self.update_curve,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Live update while dragging
        self.a_var.trace_add("write", lambda *_: self.update_curve())
        self.w_var.trace_add("write", lambda *_: self.update_curve())
        self.dp_var.trace_add("write", lambda *_: self.update_curve())

    def _create_slider(
        self,
        text: str,
        variable: tk.DoubleVar,
        minimum: float,
        maximum: float,
        row: int,
    ):
        ttk.Label(self.root, text=text).grid(
            row=row,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        ttk.Scale(
            self.root,
            variable=variable,
            from_=minimum,
            to=maximum,
            orient="horizontal",
            length=300,
        ).grid(
            row=row,
            column=1,
            padx=5,
            pady=5,
        )

    def update_curve(self):
        self.plotter.setCurve(
            self.a_var.get(),
            self.w_var.get(),
            self.dp_var.get(),
        )
        self.plotter.update()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    plotter = CurvePlotter()
    plotter.show()

    controller = CurveController(plotter)
    controller.run()
