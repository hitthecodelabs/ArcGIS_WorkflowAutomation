import math

def sort_clockwise(points):
    """
    Sorts a list of 2D points (UTM coordinates) in clockwise order.

    Args:
        points: A list of 2D points, where each point is a list [x, y].

    Returns:
        A new list containing the points sorted in clockwise order.
        Returns an empty list if the input list is empty or None.
        Returns the original list if it contains fewer than 3 points (as clockwise
        order is not well-defined for fewer than 3 points).
    """

    if not points:
        return []  # Handle empty input list

    if len(points) < 3:
        return points[:]  # Return a copy for lists with fewer than 3 points

    # 1. Calculate the centroid (center point) of all points.
    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)
    centroid = (center_x, center_y)

    # 2. Define a function to calculate the angle between a point and the centroid.
    def calculate_angle(point):
        """Calculates the angle in radians between the centroid and the point."""
        dx = point[0] - centroid[0]
        dy = point[1] - centroid[1]
        return math.atan2(dy, dx)

    # 3. Sort the points based on their angle with the centroid.
    #    We use a key function with calculate_angle.  We also adjust the angle
    #    to be in the range [0, 2*pi] instead of [-pi, pi] for easier clockwise sorting
    #    and reverse the order to make the sorting clockwise.

    sorted_points = sorted(points, key=lambda p: (calculate_angle(p) + 2 * math.pi) % (2 * math.pi), reverse=False)

    # Find the smallest angle point and its index
    smallest_angle_index = 0
    smallest_angle = (calculate_angle(sorted_points[0]) + 2 * math.pi) % (2 * math.pi)
    for i, point in enumerate(sorted_points[1:],1): # enumerate from the second item
      angle = (calculate_angle(point) + 2 * math.pi) % (2 * math.pi)
      if angle < smallest_angle:
        smallest_angle = angle
        smallest_angle_index = i

    #Rotate the array, to move the smallest angle first
    sorted_points = sorted_points[smallest_angle_index:] + sorted_points[:smallest_angle_index]
    
    # Check if the sorting direction is really clockwise
    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    
    if cross_product(sorted_points[0], sorted_points[1], sorted_points[2]) > 0:  # Counter-Clockwise
        sorted_points.reverse()
    
    return sorted_points
