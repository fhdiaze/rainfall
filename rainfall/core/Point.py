import math


class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        """Creates a point

        :param x: The x of the point
        :param y: The y of the point
        """
        self.x = x
        self.y = y

    def __str__(self):
        """Converts self point to its string representation

        :return: Point as string
        """
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        """Checks if self point is equal to other point

        :param other: The point to be compared
        :return: True if self is equal to other, False otherwise
        """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """Checks if self point is different to other point

        :param other: The point to be compared
        :return: True if self is different to other, False otherwise
        """
        return self.x != other.x or self.y == other.y

    def __add__(self, other):
        """Calculates the sum between self and other points

        :rtype: Point
        :return: A new point equal to the sum of self and other points
        """
        nx = self.x + other.x
        ny = self.y + other.y

        return Point(nx, ny)

    def __sub__(self, other):
        """Calculates the sum between self and other points

        :rtype: Point
        :return: A new point equal to the subtraction of self and other points
        """
        nx = self.x - other.x
        ny = self.y - other.y

        return Point(nx, ny)

    def __neg__(self):
        """Calculates the negative of self point

        :rtype: Point
        :return: A new point equal to the negative version of self
        """
        return Point(-self.x, -self.y)

    def __abs__(self):
        """Calculates the absolute value of self point

        :rtype: Point
        :return: A new point equal to the absolute version of self
        """
        return Point(abs(self.x), abs(self.y))

    def det(self, other):
        """Calculates the determinant of the matrix [[self.x, self.y], [other.x, other.y]]

        :rtype: int
        :return: The determinant of the 2x2 matrix
        """
        return (self.x * other.y) - (self.y * other.x)
