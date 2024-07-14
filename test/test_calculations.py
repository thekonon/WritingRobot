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
        ((100, 100, 100, 100, 50), [100, 100],  [1.57, 0.00, 0.13, 2.08]),  #Test 0
        ((100, 100, 100, 100, 50), [25, 150],   [2.11, 0.70, 1.02, 2.44]),  #Test 1
        ((100, 100, 100, 50, 50),  [42.5, 135], [2.00, 0.48, 1.32, 2.27]),  #Test 2
        ((80, 100, 100, 50, 50),   [42.5, 135], [2.00, 0.7, 1.30, 2.3]),    #Test 3
        ((90, 100, 110, 120, 50),  [25, 10],    [2.2,  5.6,  0.9, 3.8]),    #Test 4
        ((90, 100, 110, 120, 50),  [25, -10],    [1.4,  4.8,  1.7, 4.6]),   #Test 5
        ((90, 100, 110, 120, 50),  [-10, -10],    [6.22, 3.2, 1.84, 4.35]), #Test 6
        # Additional test cases
        # 1. Minimum Reach (All lengths zero)
        ((0, 0, 0, 0, 0), [0, 0], [0, 0, 0, 0]),                            #Test 7
        # 2. Maximum Reach
        ((100, 100, 100, 100, 50), [200, 0], [0, 0, 5.56, 0.7]),            #Test 8
        # 3. Boundary Conditions
        ((100, 100, 100, 100, 50), [100, 100], [1.57, 0.00, 0.13, 2.08]),   #Test 9
        ((100, 100, 100, 100, 50), [150, 0], [0.72, 5.56, 5.2, 1.05]),      #Test 10
        # 4. Negative Coordinates
        ((100, 100, 100, 100, 50), [-50, -50], [5.1, 2.7, 2.6, 4.6])   #Test 11
    ])
def test_calculate_angles(lenghts, end_points, expected_result):
    robot = Robot(lengths=lenghts, initial_position = end_points)
    assert pytest.approx(robot.phi, rel=0.04) == expected_result
    
def test_get_motor_angles():
    robot = Robot(lengths=(100, 100, 100, 100, 50),
                  initial_position = [100, 100])
    assert robot.get_motor_angles([100, 100]) == (1.5707963267948966, 0.12955216714882256)
    
if __name__ == "__main__":
    print("Running")