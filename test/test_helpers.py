import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

<<<<<<< HEAD
=======

>>>>>>> af93b70ee9220aca460f82bb33d5fe87c9b9f018
import gui.control._helpers as _helpers

def test_map_to_data():
    from_value_min = _helpers.Calculations._FROM_MIN_VALUE
    from_value_max = _helpers.Calculations._FROM_MAX_VALUE
    to_value_min = _helpers.Calculations._MIN_VALUE
    to_value_max = _helpers.Calculations._MAX_VALUE
    
    assert _helpers.Calculations.map_value(from_value_min) == to_value_min
    assert _helpers.Calculations.map_value(from_value_max) == to_value_max
    
def test_value_to_hex():
    assert _helpers.Calculations.value_to_hex(347.36) == [0, 1, 91, 36]
    assert _helpers.Calculations.value_to_hex(-347.36) == [1, 1, 91, 36]
    assert _helpers.Calculations.value_to_hex(0) == [0,0,0,0]

def test_value_to_hex_2():
    # Normal cases
    assert _helpers.Calculations.value_to_hex_2(312.1234564) == [1, 56, 4, 210]
    assert _helpers.Calculations.value_to_hex_2(0) == [0, 0, 0, 0]
    assert _helpers.Calculations.value_to_hex_2(360) == [0, 0, 0, 0]
    assert _helpers.Calculations.value_to_hex_2(720) == [0, 0, 0, 0]
    assert _helpers.Calculations.value_to_hex_2(180) == [0, 180, 0, 0]
    
    # Edge cases
    assert _helpers.Calculations.value_to_hex_2(359.9999) == [1, 103, 39, 15]
    assert _helpers.Calculations.value_to_hex_2(360.0001) == [0, 0, 0, 1]
    assert _helpers.Calculations.value_to_hex_2(720.0001) == [0, 0, 0, 1]

    # Negative input
    assert _helpers.Calculations.value_to_hex_2(-90) == [1, 14, 0, 0]

    # Large input
    assert _helpers.Calculations.value_to_hex_2(1000000) == [1, 24, 0, 0]
