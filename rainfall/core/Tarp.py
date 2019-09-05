from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["lower", "higher"]

    def __init__(self, lower: Point, higher: Point):
        self.lower = lower
        self.higher = higher

    def __str__(self):
        return str.format("<{}, {}>", self.lower, self.higher)

    def slope(self):
        v = self.clockwise()

        return v.y / v.x

    def clockwise(self):
        return self.higher - self.lower

    def counterclockwise(self):
        return self.lower - self.higher

    def intersect(self, other):
        resp = False
        r = self.clockwise()
        s = other.clockwise()
        rxs = r.det(s)
        sxr = s.det(r)

        if self.overlap(other) < Point.EPSILON < abs(rxs):
            t = (other.tail - self.tail).det(s) / rxs
            u = (self.tail - other.tail).det(r) / sxr

            resp = (0.0 < t < 1.0 and 0.0 < u < 1.0)
