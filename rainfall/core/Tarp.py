from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["lower", "higher"]

    def __init__(self, lower: Point, higher: Point):
        self.lower = lower
        self.higher = higher

    def __str__(self):
        return str.format("<{}, {}>", self.lower, self.higher)

    def __lt__(self, other):
        if self.overlaps(other):
            if self.slope() > 0 and other.slope() > 0:
                resp = -self.lower.x < -other.lower.x
            elif self.slope() < 0 and other.slope() < 0:
                resp = self.lower.x < other.lower.x
            else:
                resp = self.lower.y < other.lower.y
        else:
            resp = self.lower.y < other.lower.y

        return resp

    def __neg__(self):
        return Tarp(-self.lower, -self.higher)

    def slope(self):
        v = self.clockwise()

        return v.y / v.x

    def clockwise(self):
        return self.higher - self.lower

    def counterclockwise(self):
        return self.lower - self.higher

    def overlaps(self, other):
        self = Tarp(Point(self.higher.x, self.lower.y),
                    Point(self.lower.x, self.higher.y)) if self.slope() < 0 else self
        other = Tarp(Point(other.higher.x, other.lower.y),
                     Point(other.lower.x, other.higher.y)) if other.slope() < 0 else other

        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(self.lower.x, other.lower.x)
        yA = max(self.lower.y, other.lower.y)
        xB = min(self.higher.x, other.higher.x)
        yB = min(self.higher.y, other.higher.y)

        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        return interArea > 0

    def intersect(self, other):
        """Checks whether two tarps intersect with each other. It does not include extreme points.
        Note: Based in http://ideone.com/PnPJgb

        :param other: the other tarp
        :return: True if the self intersects with other, False otherwise
        """
        cmp = other.lower - self.lower
        r = self.clockwise()
        s = other.clockwise()

        cmp_x_r = cmp.det(r)
        cmp_x_s = cmp.det(s)
        r_x_s = r.det(s)

        if r_x_s == 0:
            # Lines are parallel.
            resp = False
        else:
            r_x_sr = 1.0 / r_x_s
            t = cmp_x_s * r_x_sr
            u = cmp_x_r * r_x_sr

            resp = (0.0 < t < 1.0 and 0.0 < u <= 1.0)

        return resp
