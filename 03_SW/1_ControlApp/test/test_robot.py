import os
import sys
import pytest
import math
from unittest.mock import patch

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from src.mechanics.robot import Robot

@pytest.fixture
def robot_instance():
    # Fixture to create a Robot instance with default settings
    lengths = (90, 100, 110, 120, 50)
    initial_position = (50, 100.0)
    return Robot(lengths=lengths, initial_position=initial_position)

def test_property_assigments_r_m():
    robot = Robot(lengths=(100, 100, 100, 100, 50))
    robot.r_m = [100, 100]
    assert robot.r_m == [100, 100]
    
def test_property_assigments_lengths():
    robot = Robot(lengths=(80, 90, 100, 110, 50))
    assert robot.settings.LENGTHS == (80, 90, 100, 110, 50)

@pytest.mark.parametrize(
    "lenghts, end_points, expected_result, raises_exception", 
    [
        # Valid cases
        ((100, 100, 100, 100, 50), [100, 100],  [1.57, 0.00, 0.13, 2.08], False),  # Test 0
        ((100, 100, 100, 100, 50), [25, 150],   [2.11, 0.70, 1.02, 2.44], False),  # Test 1
        ((100, 100, 100, 50, 50),  [42.5, 135], [2.00, 0.48, 1.32, 2.27], False),  # Test 2
        ((80, 100, 100, 50, 50),   [42.5, 135], [2.00, 0.7, 1.30, 2.3],  False),  # Test 3
        ((90, 100, 110, 120, 50),  [25, 10],    [2.2,  5.6,  0.9, 3.8],  False),  # Test 4
        ((90, 100, 110, 120, 50),  [25, -10],   [1.4,  4.8,  1.7, 4.6],  False),  # Test 5
        ((90, 100, 110, 120, 50),  [-10, -10],  [6.22, 3.2, 1.84, 4.35], False),  # Test 6

        # Edge cases
        # 1. Minimum Reach (All lengths zero)
        ((0, 0, 0, 0, 0), [0, 0], [0, 0, 0, 0], True),                           # Test 7
        # 2. Maximum Reach (Beyond possible reach)
        ((100, 100, 100, 100, 50), [500, 500], None, True),                      # Test 8
        # 3. Invalid lengths (negative lengths)
        ((-100, 100, 100, 100, 50), [100, 100], None, True),                     # Test 9
        # 4. Invalid end points (outside possible range)
        ((100, 100, 100, 100, 50), [1000, 1000], None, True),                    # Test 10
    ])
def test_calculate_angles(lenghts, end_points, expected_result, raises_exception):
    if raises_exception:
        with pytest.raises(ValueError):
            robot = Robot(lengths=lenghts, initial_position=end_points)
    else:
        robot = Robot(lengths=lenghts, initial_position=end_points)
        assert pytest.approx(robot._internal_angles, rel=0.04) == expected_result
        
def test_set_motor_angles_valid_floats(robot_instance):
    robot_instance.set_motor_angles(2.196178244710251, 0.9211712501423452)
    #[25, 10]
    assert robot_instance.get_end_point() == (25, 10)










"""
def test_set_motor_angles_valid_ints(robot_instance):
    with patch.object(robot_instance, '_calculate_end_point', return_value=[2.0, 3.0]) as mock_calc:
        robot_instance.set_motor_angles(2.196178244710251, 0.9211712501423452)
        mock_calc.assert_called_once_with(1, 2)
        assert robot_instance.get_end_point() == (25, 10)


def test_set_motor_angles_one_none(robot_instance):
    with patch.object(robot_instance, '_calculate_end_point', return_value=[2.0, 3.0]) as mock_calc:
        robot_instance.set_motor_angles(None, 1.0)
        mock_calc.assert_called_once_with(robot_instance._internal_angles[0], 1.0)
        assert robot_instance.get_end_point() == (2.0, 3.0)


def test_set_motor_angles_both_none(robot_instance):
    with patch.object(robot_instance, '_calculate_end_point', return_value=[2.0, 3.0]) as mock_calc:
        robot_instance.set_motor_angles(None, None)
        mock_calc.assert_called_once_with(robot_instance._internal_angles[0], robot_instance._internal_angles[2])
        assert robot_instance.get_end_point() == (2.0, 3.0)


def test_set_motor_angles_invalid_first_argument(robot_instance):
    with pytest.raises(ValueError, match="First input argument must be float / int"):
        robot_instance.set_motor_angles("invalid", 1.0)


def test_set_motor_angles_invalid_second_argument(robot_instance):
    with pytest.raises(ValueError, match="Second input argument must be float / int"):
        robot_instance.set_motor_angles(1.0, "invalid")


def test_set_motor_angles_invalid_both_arguments(robot_instance):
    with pytest.raises(ValueError, match="First input argument must be float / int"):
        robot_instance.set_motor_angles("invalid", "invalid")
        
        """