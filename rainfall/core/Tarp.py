from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["lower", "higher"]

    def __init__(self, lower: Point, higher: Point):
        self.lower = lower
        self.higher = higher

    def __str__(self):
        return str.format("<{}, {}>", self.lower, self.higher)

    def __lt__(self, other):
        resp = False
        slx, srx = sorted((self.lower.x, self.higher.x))
        olx, orx = sorted((other.lower.x, other.higher.x))

        if slx < olx < srx or slx < orx < srx:
            start_overlap = max(slx, olx)
            om, ob = other.line_equation()
            sm, sb = self.line_equation()

            if om == sm:
                resp = sb < ob
            else:
                intersection_x = (ob - sb) / (sm - om)
                if sm > om:
                    resp = (start_overlap < intersection_x)
                else:
                    resp = (start_overlap > intersection_x)
        else:
            resp = (self.lower.y < other.lower.y) or (slx < olx)

        return resp

    def slope(self):
        v = self.clockwise()

        return v.y / v.x

    def clockwise(self):
        return self.higher - self.lower

    def line_equation(self):
        m = self.slope()
        b = self.lower.y - m * self.lower.x

        return m, b
