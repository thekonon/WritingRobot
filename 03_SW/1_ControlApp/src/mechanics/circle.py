import math
from typing import Optional, Tuple

class Circle:
    def __init__(self, midpoint: tuple, radius: float):
        self.mid_point: tuple = midpoint
        self.radius: float = radius
        
    def intersection(self, circle: 'Circle') -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        # Coordinates and radii of the circles
        x1, y1 = self.mid_point
        r1 = self.radius
        x2, y2 = circle.mid_point
        r2 = circle.radius
        
        # Distance between the centers of the two circles
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # Check for special cases
        if d > r1 + r2 or d < abs(r1 - r2) or (d == 0 and r1 == r2):
            raise ValueError("No intersection found")  # Circles do not intersect or are coincident
        
        # Finding the intersection points
        a = (r1**2 - r2**2 + d**2) / (2 * d)
        h = math.sqrt(r1**2 - a**2)
        
        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d
        
        intersection1 = (x3 + h * (y2 - y1) / d, y3 - h * (x2 - x1) / d)
        intersection2 = (x3 - h * (y2 - y1) / d, y3 + h * (x2 - x1) / d)
        
        # Return a tuple with both intersection points
        return (intersection1, intersection2)
    
if __name__ == "__main__":
    c1 = Circle((0, 0), 10)
    c2 = Circle((0, 10), 10)
    intersections = c1.intersection(c2)
    print("Intersections:", intersections)
