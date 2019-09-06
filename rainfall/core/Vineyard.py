import math
import matplotlib.pyplot as plt
from typing import List
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp


class Vineyard(object):
    MAX_X = 10**9
    MAX_Y = 10**9
    MAX_TARPS = 5 * 10**5
    __slots__ = ["start", "end", "tarps", "min_x", "min_y", "max_x", "max_y"]

    def __init__(self, start: int, end: int, tarps: List[Tarp]):
        self.start = start
        self.end = end
        self.tarps = tarps
        self.min_x, self.min_y, self.max_x, self.max_y = self.tarps_box()

    def __str__(self):
        tarps = ", ".join([str(t) for t in self.tarps])
        return str.format("<{}, {}> : [{}]", self.start, self.end, tarps)

    def min_punctures(self):
        return min([self.punctures(x, self.max_y) for x in range(self.start, self.end+1)])

    def punctures(self, x, y):
        p = -1

        if self.min_x < x < self.max_x and y > self.min_y:
            # The point could be over tarps
            tarp = self.cross_tarp(Tarp(Point(x, y - 1), Point(x, y)))

            if tarp is not None:
                slope = tarp.slope()
                nx = x - 1 if slope > 0 else x + 1
                p = min(1 + self.punctures(x, y - 1), self.punctures(nx, y))
            else:
                p = self.punctures(x, y - 1)
        elif self.start <= x <= self.end:
            p = 0
        else:
            p = Vineyard.MAX_TARPS

        return p

    def cross_tarp(self, tt):
        for t in self.tarps:
            if t.intersect(tt):
                return t

        return None

    def tarps_box(self):
        min_x, min_y, max_x, max_y = Vineyard.MAX_X, Vineyard.MAX_Y, 0, 0,

        for tarp in self.tarps:
            min_x = min(min_x, tarp.lower.x, tarp.higher.x)
            min_y = min(min_y, tarp.lower.y, tarp.higher.y)
            max_x = max(max_x, tarp.lower.x, tarp.higher.x)
            max_y = max(max_y, tarp.lower.y, tarp.higher.y)

        return min_x, min_y, max_x, max_y

    def plot(self):
        plt.interactive(False)
        plt.show(block=True)
        plt.axes()

        line = plt.Line2D([self.start, self.end], [0, 0], 4, color='green')
        plt.gca().add_line(line)

        for tarp in self.tarps:
            xs = [tarp.lower.x, tarp.higher.x]
            ys = [tarp.lower.y, tarp.higher.y]
            line = plt.Line2D(xs, ys, 2, color='black')
            plt.gca().add_line(line)

        plt.axis('scaled')
        plt.show()
