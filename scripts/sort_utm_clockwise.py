import math

def sort_utm_clockwise(utm_x, utm_y):
    """
    Sorts UTM coordinates clockwise.

    Args:
        utm_x: A list of UTM x-coordinates.
        utm_y: A list of UTM y-coordinates.

    Returns:
        A list of tuples, where each tuple is a (utm_x, utm_y) coordinate,
        sorted in clockwise order. Returns an empty list if input lists are empty.
    """
    if not utm_x or not utm_y or len(utm_x) != len(utm_y):
        return []  # Handle empty or invalid input

    coords = [(utm_x[i], utm_y[i]) for i in range(len(utm_x))]

    if len(coords) <= 2:
        return coords  # No need to sort if 2 or fewer points

    # 1. Calculate the centroid (center of mass) of the coordinates.
    center_x = sum(x for x, y in coords) / len(coords)
    center_y = sum(y for x, y in coords) / len(coords)

    # 2. Define a function to calculate the angle of each point relative to the centroid.
    def angle_to_centroid(coord):
        x, y = coord
        return math.atan2(y - center_y, x - center_x)

    # 3. Sort the coordinates based on their angles in descending order.
    #    Descending order for atan2 usually results in clockwise sorting.
    sorted_coords = sorted(coords, key=angle_to_centroid, reverse=True)

    return sorted_coords
