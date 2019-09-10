import math


class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y == other.y

    def __add__(self, other):
        nx = self.x + other.x
        ny = self.y + other.y

        return Point(nx, ny)

    def __sub__(self, other):
        nx = self.x - other.x
        ny = self.y - other.y

        return Point(nx, ny)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def det(self, other):
        return (self.x * other.y) - (self.y * other.x)
