from rainfall.core.Point import Point


class Tarp(object):
    __slots__ = ["tail", "head"]

    def __init__(self, tail: Point, head: Point):
        self.tail = tail
        self.head = head

    def __str__(self):
        return str.format("<{}, {}>", self.tail, self.head)

    def is_left(self, p: Point):
        """Evaluates if a point is left, right or on the segment

        :param p: the point to check
        :return: >0 for p left of the segment
                 =0 for p on the segment
                 <0 for p right of the segment
        """
        return (self.head.x - self.tail.x) * (p.y - self.tail.y) - (p.x - self.tail.x) * (self.head.y - self.tail.y)

    def clockwise(self):
        return self.head - self.tail

    def counterclockwise(self):
        return self.tail - self.head

    def length(self):
        return self.clockwise().norm()

    def is_unlike(self, other):
        return self.clockwise().is_unlike(other.clockwise())

    def overlap(self, other):
        overlap = 0.0
        tl = self.length() + other.length()
        ts = self.tail - other.tail
        hs = self.head - other.head

        if self.is_unlike(other):
            # check if there is overlap
            if tl - ts.norm() > Point.EPSILON and tl - hs.norm() > Point.EPSILON:
                s = hs if ts.norm() > hs.norm() else ts
                s2 = other.clockwise()

                if hs.is_unlike(s2) or ts.is_unlike(s2):
                    overlap += min(ts.norm(), hs.norm(), self.length(), other.length())

        return overlap
