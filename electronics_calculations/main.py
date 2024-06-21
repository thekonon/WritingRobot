"""
Test the Cutof frequencies for filtering
"""

from abc import ABC, abstractmethod
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import List

class Filter(ABC):
    """Abstract class for all filters"""
    def __init__(self) -> None:
        print("Filter initialized")
    
    @abstractmethod
    def get_bode(self) -> tuple:
        """Return tuple of angualr speed, magnitude and frequency shift"""
    @abstractmethod
    def _calculater_cut_of_frequency(self) -> float:
        """Return fc - cut of frequency in Hz"""
        
class RCFilter(Filter):
    """Implementation for RC filter"""
    def __init__(self,
                 resistance: float,
                 capacitance: float) -> None:
        super().__init__()
        self.resistance = resistance
        self.capacitance = capacitance
        
    def _calculater_cut_of_frequency(self) -> float:
        return 1 / (2 * 3.14 * self.resistance *self.capacitance)
    
    def get_bode(self) -> tuple:
        sys = signal.TransferFunction([1], [1, self.resistance*self.capacitance])
        w, mag, phase = signal.bode(sys)
        return (w, mag, phase)

class Plotter:
    def __init__(self) -> None:
        pass
    
    def _create_single_axes(self):
        self.single_ax: Axes = plt.axes()
        
    def _create_double_axes(self):
        self.figure: Figure
        self.axes: List[Axes]
        self.figure, self.axes = plt.subplots(2,1)
        
        
    def plot(self, x: list, y: list):
        # Create a new axis if they do not exist
        if not hasattr(self, 'single_ax'):
            self._create_single_axes()
        self.single_ax.plot(x, y)
        
    def semi_plot(self, x: list, y: list):
        # Create a new axis if they do not exist
        if not hasattr(self, 'single_ax'):
            self._create_single_axes()
        self.single_ax.semilogx(x, y)
        
    def bode_plot(self, 
                  angular_velocity: tuple, 
                  magnitude: tuple, 
                  phase_shift: tuple):
        # Create a new axis if they do not exist
        if not hasattr(self, 'axes'):
            self._create_double_axes()
        
        # First axis
        self.axes[0].semilogx(angular_velocity, magnitude)
        self.axes[0].grid(linewidth=2, linestyle='-', which='both')
        
        # Second axis
        self.axes[1].semilogx(angular_velocity, phase_shift)
        self.axes[1].grid(linewidth=2, linestyle='-', which='both')

if __name__ == "__main__":
    rc_filter = RCFilter(100, 47e-6)
    plotter = Plotter()
    w, a, p = rc_filter.get_bode()
    plotter.bode_plot(w, a, p)
    plt.show()
    
        