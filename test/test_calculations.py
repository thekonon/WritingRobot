import os
import sys
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from gui.mechanics.robot import Robot

def test_property_assigments_r_m():
    robot = Robot(lengths=(100, 100, 100, 100, 50))
    robot.r_m = [100, 100]
    assert robot.r_m == [100, 100]
    
def test_property_assigments_lengths():
    robot = Robot(lengths=(80, 90, 100, 110, 50))
    assert robot.lengths == (80, 90, 100, 110, 50)

@pytest.mark.parametrize(
        "lenghts, end_points, expected_result", 
    [
        ((100, 100, 100, 100, 50), [100, 100],  [1.57, 0.13, 0.00, 2.08]),
        ((100, 100, 100, 100, 50), [25, 150],   [2.11, 1.02, 0.70, 2.44]),
        ((100, 100, 100, 50, 50),  [42.5, 135], [2.00, 1.32, 0.48, 2.27]),
        ((80, 100, 100, 50, 50),   [42.5, 135], [2.02, 1.32, 0.68, 2.27])
    ])
def test_calculate_angles(lenghts, end_points, expected_result):
    robot = Robot(lengths=lenghts)
    robot.r_m = end_points
    assert pytest.approx(robot.phi, rel=0.05) == expected_result
    
def test_get_motor_angles():
    robot = Robot(lengths=(100, 100, 100, 100, 50))
    robot.r_m = [100, 100]
    assert robot.get_motor_angles([100, 100]) == (1.5707963267948966, 0.12955216714882256)
    
if __name__ == "__main__":
    print("Running")