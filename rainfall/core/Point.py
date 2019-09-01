import math


class Point:
    EPSILON = 0.0000001
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.y and self.y == other.y

    def __sub__(self, other):
        nx = self.x - other.x
        ny = self.y - other.y

        return Point(nx, ny)

    def right(self, other):
        return self.x > other.x
