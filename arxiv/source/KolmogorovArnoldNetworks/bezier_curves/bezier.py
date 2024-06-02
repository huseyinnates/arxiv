import math
import numpy as np

def bezier_curve(points, num_points=1000, loop=False):
    if loop:
        points = points + [points[0]]
    n = len(points) - 1
    curve_points = []
    for t in np.linspace(0, 1, num_points):
        x, y = 0, 0
        for i, point in enumerate(points):
            bernstein_poly = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (t ** i) * ((1 - t) ** (n - i))
            x += point[0] * bernstein_poly
            y += point[1] * bernstein_poly
        curve_points.append((int(x), int(y)))
    return curve_points
