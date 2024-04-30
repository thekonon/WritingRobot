import os
import sys

# Get the absolute path of the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import modules relative to the parent directory
from mechanics import Robot

def test_property_assigments_r_m():
    robot = Robot(lengths=(100, 100, 100, 100, 50))
    robot.r_m = [100, 100]
    assert robot.r_m == [100, 100]
    
def test_calculate_angles():
    robot = Robot(lengths=(100, 100, 100, 100, 50))
    robot.r_m = [100, 100]
    assert robot.phi == [1.5707963267948966, 0.12955216714882256, 0.0, 2.084745268439358]
    
    robot.r_m = [25, 150]
    assert robot.phi == [2.112599377267488, 1.0289932763223057, 0.698695921493052, 2.442896732096741]