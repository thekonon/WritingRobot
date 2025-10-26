import math
class RobotCalculationMixin:
    @staticmethod
    def law_of_cosine_angle(a: float, b: float, c: float) -> float:
        """Return angle opposing side A (alfa angle in radians)"""
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("All numbers must be positive")
        if (a + b) < c or (a + c) < b or (b + c) < a:
            raise ValueError("Triangle inequality is not met")

        return math.acos((b**2 + c**2 - a**2) / (2 * b * c))

    
    @staticmethod
    def atan2(y, x) -> float:
        if x == 0 and y == 0:
            raise ValueError("Both x and y can not be 0 for arctan function")
        angle = math.atan2(y, x)
        if angle < 0:
            angle += 2*math.pi
        return angle
    
    @staticmethod
    def check_if_point_is_in_both_circles(point: tuple|list, r1: float, r2: float, l5: float) -> bool:
        def _calculate_distance_between_points(point1: tuple|list, point2: tuple|list) -> float:
            dx = point1[0] - point2[0]
            dy = point1[1] - point2[1]
            return (dx**2+dy**2)**0.5
        distance_to_first_point = _calculate_distance_between_points(point, (0, 0))
        distance_to_second_point = _calculate_distance_between_points(point, (l5, 0))
        if distance_to_first_point <= r1 and distance_to_second_point <= r2:
            return True
        return False
    
    @staticmethod
    def find_circle_intersections(x1, y1, r1, x2, y2, r2):
        # Calculate the distance between the centers
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Check if there are no intersections
        if d > r1 + r2 or d < abs(r1 - r2) or (d == 0 and r1 == r2):
            raise ValueError("No intersection point found - no solution")  # No intersections or circles are coincident
        
        # Calculate the x coordinate of the intersection points
        a = (r1**2 - r2**2 + d**2) / (2 * d)
        h = math.sqrt(r1**2 - a**2)
        
        # Calculate the point P2 which is the point where the line through the circle intersection points crosses the line between the circle centers
        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d
        
        # Calculate the intersection points
        intersection1 = (x3 + h * (y2 - y1) / d, y3 - h * (x2 - x1) / d)
        intersection2 = (x3 - h * (y2 - y1) / d, y3 + h * (x2 - x1) / d)
        
        if intersection1[1] < intersection2[1]:
            return intersection2
        return intersection1