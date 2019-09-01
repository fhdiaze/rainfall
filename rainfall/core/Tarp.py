from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["lower", "higher"]

    def __init__(self, lower: Point, higher: Point):
        self.lower = lower
        self.higher = higher

    def __str__(self):
        return str.format("<{}, {}>", self.lower, self.higher)

    def slope(self):
        v = self.higher - self.lower

        return v.y / v.x
