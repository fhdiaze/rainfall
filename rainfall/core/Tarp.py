from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["lower", "higher"]

    def __init__(self, lower: Point, higher: Point):
        self.lower = lower
        self.higher = higher

    def __str__(self):
        """Converts self tarp to its string representation

        :return: Tarp as string
        """
        return str.format("<{}, {}>", self.lower, self.higher)

    def __lt__(self, other):
        """Check if self is lower than other

        :param other: The other tarp to be compared
        :return: True if self is lower than other, False otherwise
        """
        resp = False
        slx, srx = sorted((self.lower.x, self.higher.x))
        olx, orx = sorted((other.lower.x, other.higher.x))

        if slx < olx < srx or slx < orx < srx:
            start_overlap = max(slx, olx)
            other_m, other_b = other.line_equation()
            self_m, self_b = self.line_equation()

            if other_m == self_m:
                resp = self_b < other_b
            else:
                intersection_x = (other_b - self_b) / (self_m - other_m)
                if self_m > other_m:
                    resp = (start_overlap < intersection_x)
                else:
                    resp = (start_overlap > intersection_x)
        else:
            resp = (self.lower.y < other.lower.y) or (self.lower.y == other.lower.y and slx < olx)

        return resp

    def slope(self):
        """Calculate the slope of the tarp

        :return: The slope of the tarp
        """
        v = self.clockwise()

        return v.y / v.x

    def clockwise(self):
        """Calculates the vector from lower to higher point

        :return: The clockwise vector
        """
        return self.higher - self.lower

    def line_equation(self):
        """Calculates the slope and intersection with y axis of the tarp

        :return: The slope and the intersection with the y axis
        """
        m = self.slope()
        b = self.lower.y - m * self.lower.x

        return m, b
