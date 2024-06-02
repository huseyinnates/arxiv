import numpy as np

class BSpline:
    def __init__(self, control_points, degree=3, num_points=300):
        self.control_points = control_points
        self.degree = degree
        self.num_points = num_points
        self.knot_vector = self.create_knot_vector()

    def create_knot_vector(self):
        n = len(self.control_points)
        k = self.degree
        knots = [0] * (k + 1) + list(range(1, n - k)) + [n - k] * (k + 1)
        return np.array(knots, dtype='float')

    def basis_function(self, i, k, t, knots):
        if k == 0:
            return 1.0 if knots[i] <= t < knots[i + 1] else 0.0
        else:
            denom1 = knots[i + k] - knots[i]
            denom2 = knots[i + k + 1] - knots[i + 1]
            term1 = ((t - knots[i]) / denom1) * self.basis_function(i, k - 1, t, knots) if denom1 > 0 else 0
            term2 = ((knots[i + k + 1] - t) / denom2) * self.basis_function(i + 1, k - 1, t, knots) if denom2 > 0 else 0
            return term1 + term2

    def calculate(self):
        n = len(self.control_points)
        m = len(self.knot_vector)
        u = np.linspace(self.knot_vector[self.degree], self.knot_vector[-self.degree - 1], self.num_points)
        curve = np.zeros((self.num_points, 2))
        for j in range(self.num_points):
            t = u[j]
            point = np.zeros(2)
            for i in range(n):
                b = self.basis_function(i, self.degree, t, self.knot_vector)
                point += b * np.array(self.control_points[i])
            curve[j] = point
        return curve

    def update_knot_vector(self, new_knots):
        if len(new_knots) == len(self.knot_vector):
            self.knot_vector = np.array(new_knots, dtype='float')

