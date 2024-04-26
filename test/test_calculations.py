import os
import sys

# Get the absolute path of the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import modules relative to the parent directory
from control import _calculations

def test_map_to_data():
    from_value_min = _calculations.Calculations._FROM_MIN_VALUE
    from_value_max = _calculations.Calculations._FROM_MAX_VALUE
    to_value_min = _calculations.Calculations._MIN_VALUE
    to_value_max = _calculations.Calculations._MAX_VALUE
    
    assert _calculations.Calculations.map_value(from_value_min) == to_value_min
    assert _calculations.Calculations.map_value(from_value_max) == to_value_max
    
def test_value_to_hex():
    assert _calculations.Calculations.value_to_hex(347.36) == [0, 1, 91, 36]
    assert _calculations.Calculations.value_to_hex(-347.36) == [1, 1, 91, 36]
    assert _calculations.Calculations.value_to_hex(0) == [0,0,0,0]
    