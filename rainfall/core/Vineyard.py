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

    def punctures(self, f):
        punctures = (f(x, self.max_y) for x in range(self.start, self.end + 1))
        p = next(punctures)
        np = p

        while p > 0 and np is not None:
            np = next(punctures, None)
            p = np if np is not None and np < p else p

        return p

    def recursive_punctures(self):
        punctures = self.punctures(lambda x, y: self.min_punctures(x, y))

        return punctures

    def memo_punctures(self):
        m = dict()
        punctures = self.punctures(lambda x, y: self.min_punctures_with_memo(m, x, y))

        return punctures

    def iterative_punctures(self):
        punctures = self.punctures(lambda x, y: self.min_iter_punctures(x, y))

        return punctures

    def min_punctures(self, x, y):
        p = -1

        if self.min_x < x < self.max_x and y > self.min_y:
            # The point could be over tarps
            intersected = self.cross_tarp(Tarp(Point(x, y - 1), Point(x, y)))

            if intersected:
                slope = intersected[0].slope()
                nx = x - 1 if slope > 0 else x + 1
                make_puncture = len(intersected) + self.min_punctures(x, y - 1)
                no_puncture = self.min_punctures(nx, y)
                p = min(make_puncture, no_puncture)
            else:
                p = self.min_punctures(x, y - 1)
        elif self.start <= x <= self.end:
            p = 0
        else:
            p = Vineyard.MAX_TARPS

        return p

    def min_punctures_with_memo(self, m, x, y):
        p = -1

        if self.min_x < x < self.max_x and y > self.min_y:
            p = m.get((x, y), -1)

            if p == -1:
                # The point could be over tarps
                intersected = self.cross_tarp(Tarp(Point(x, y - 1), Point(x, y)))

                if intersected:
                    slope = intersected[0].slope()
                    nx = x - 1 if slope > 0 else x + 1
                    make_puncture = len(intersected) + self.min_punctures_with_memo(m, x, y - 1)
                    no_puncture = self.min_punctures_with_memo(m, nx, y)
                    p = min(make_puncture, no_puncture)
                else:
                    p = self.min_punctures_with_memo(m, x, y - 1)

                m[(x, y)] = p
        elif self.start <= x <= self.end:
            p = 0
        else:
            p = Vineyard.MAX_TARPS

        return p

    def min_iter_punctures(self, x, y):
        p = -1

        last_row = dict()
        current_row = dict()

        # Init base values
        for x in range(min(self.start, self.min_x), max(self.end, self.max_x)):
            if self.start <= x <= self.end:
                p = 0
            else:
                p = Vineyard.MAX_TARPS

            last_row[(x, self.min_y)] = p

        for y in range(self.min_y+1, self.max_y+1):
            for x in range(self.start, self.end+1):
                # The point could be over tarps
                intersected = self.cross_tarp(Tarp(Point(x, y - 1), Point(x, y)))

                if intersected:
                    slope = intersected[0].slope()
                    nx = x - 1 if slope > 0 else x + 1
                    make_puncture = len(intersected) + last_row.get((x, y - 1))
                    no_puncture = self.min_punctures_with_memo(nx, y)
                    p = min(make_puncture, no_puncture)
                else:
                    p = last_row.get((x, y - 1))

                current_row[(x, y)] = p

        return p

    def cross_tarp(self, vt):
        intersected = []
        for t in self.tarps:
            if t.intersect(vt):
                intersected.append(t)

        return intersected

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

        # Show the grid lines as dark grey lines
        plt.grid(b=True, which='major', color='#666666', linestyle='-')

        # Show the minor grid lines with very faint and almost transparent grey lines
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        plt.axis('scaled')
        plt.show()
