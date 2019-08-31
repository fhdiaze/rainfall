import math


class Point:
    EPSILON = 0.0000001
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        nx = self.x + other.x
        ny = self.y + other.y

        return Point(nx, ny)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        nx = self.x - other.x
        ny = self.y - other.y

        return Point(nx, ny)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            # Dot product
            return (self.x * other.x) + (self.y * other.y)
        else:
            # Scalar product
            return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def rotate(self, other, theta: float):
        tp = self - other
        nx = tp.x * math.cos(theta) - tp.y * math.sin(theta)
        ny = tp.y * math.cos(theta) + tp.x * math.sin(theta)
        np = Point(nx, ny) + other

        return np

    def det(self, other):
        return (self.x * other.y) - (self.y * other.x)

    def norm(self):
        return math.sqrt(self * self)

    def unit(self):
        norm = self.norm()

        return Point(self.x / norm, self.y / norm)

    def is_unlike(self, other):
        return (self.unit() + other.unit()).norm() <= Point.EPSILON

    def angle(self, other):
        """ Calculates the angle, in radians, between self and another point

        :param Point other: the other point
        :return: the anti-clockwise angle between self and other points
        """
        cos = self * other / (self.norm() * other.norm())
        sin = self.det(other) / (self.norm() * other.norm())
        theta = math.atan2(-sin, -cos) + math.pi

        return theta
