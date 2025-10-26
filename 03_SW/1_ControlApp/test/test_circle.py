import os
import sys
from math import isclose
import pytest
from typing import Optional, Tuple

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from src.mechanics.circle import Circle

def assert_tuple_almost_equal(t1, t2, places=7):
    """Helper function to compare tuples of floats with tolerance"""
    return all(isclose(a, b, abs_tol=10**-places) for a, b in zip(t1, t2))

def test_intersecting_circles():
    c1 = Circle((0, 0), 10)
    c2 = Circle((0, 10), 10)
    intersections = c1.intersection(c2)
    expected1 = (8.66025403784, 5.0)
    expected2 = (-8.66025403784, 5.0)
    assert assert_tuple_almost_equal(intersections[0], expected1)
    assert assert_tuple_almost_equal(intersections[1], expected2)

def test_non_intersecting_circles():
    c1 = Circle((0, 0), 5)
    c2 = Circle((0, 20), 5)
    with pytest.raises(ValueError):
        c1.intersection(c2)

def test_circles_within_each_other():
    c1 = Circle((0, 0), 5)
    c2 = Circle((0, 0), 3)
    with pytest.raises(ValueError):
        c1.intersection(c2)

def test_coincident_circles():
    c1 = Circle((0, 0), 5)
    c2 = Circle((0, 0), 5)
    with pytest.raises(ValueError):
        c1.intersection(c2)

def test_tangential_circles():
    c1 = Circle((0, 0), 5)
    c2 = Circle((10, 0), 5)
    intersections = c1.intersection(c2)
    expected = ((5.0, 0.0), (5.0, 0.0))
    assert assert_tuple_almost_equal(intersections[0], expected[0])
    assert assert_tuple_almost_equal(intersections[1], expected[1])