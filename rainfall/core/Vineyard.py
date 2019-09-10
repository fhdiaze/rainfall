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
        punctures = (f(x, self.max_y) for x in range(self.min_x, self.max_x + 1))
        p = self.MAX_TARPS
        np = next(punctures)
        i = self.min_x

        while p > 0 and np is not None:
            if self.start <= i <= self.end:
                p = np if np is not None and np < p else p
            np = next(punctures, None)
            i += 1

        return p

    def recursive_punctures(self):
        punctures = self.punctures(lambda x, y: self.min_punctures(x, y))

        return punctures

    def min_punctures(self, x, y):
        p = -1

        if self.min_x < x < self.max_x and y > self.min_y:
            # TODO check this condition because we change the method tarps_box()
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

    def memo_punctures(self):
        m = dict()
        punctures = self.punctures(lambda x, y: self.min_punctures_with_memo(m, x, y))

        return punctures

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

    def iterative_punctures(self):
        p = -1
        width = self.end - self.start + 1
        vertical_delta = Point(0, 1)
        horizontal_delta = Point(1, 0)

        # Init base values
        memo = [0] * width
        memo_x_range = (self.start, self.end)

        for y in range(self.min_y + 1, self.max_y + 1):
            current = []
            for x in range(memo_x_range[0], memo_x_range[1]+1):
                # The point could be over tarps
                p = Point(x, y)
                above_point = p + vertical_delta
                intersected = self.cross_tarp(Tarp(p, above_point))

                if intersected:
                    slope = intersected[0].slope()
                    horizontal_move = horizontal_delta if slope > 0 else -horizontal_delta
                    drill_cost = len(intersected)
                    slide_cost = self.cost(costs, row, next_point)

                    # Choose the best option (drill the tarp or let the rain slide)
                    cost = min(drill_cost, slide_cost)
                else:
                    cost = [0]

                self.set_cost(costs, row, p, cost)

        return min(costs[1][self.start-self.min_x:self.end-self.min_x+1])

    def cost(self, costs: List[List[int]], row, p: Point):
        # The point could be over tarps
        vertical_delta = Point(0, 1)
        horizontal_delta = Point(1, 0)
        above_point = p + vertical_delta
        intersected = self.cross_tarp(Tarp(p, above_point))

        if intersected:
            slope = intersected[0].slope()
            next_point = p + horizontal_delta + vertical_delta if slope > 0 else p - horizontal_delta
            drill_cost = len(intersected) + self.get_cost(costs, row, below_point)
            slide_cost = self.cost(costs, row, next_point)

            # Choose the best option (drill the tarp or let the rain slide)
            cost = min(drill_cost, slide_cost)
        else:
            cost = p

        self.set_cost(costs, row, p, cost)

        return cost

    def get_cost(self, costs: List[List[int]], row, p: Point):
        shift = Point(self.min_x, row)
        shifted_point = abs(p - shift)

        return costs[shifted_point.y][shifted_point.x]

    def set_cost(self, costs: List[List[int]], row, p: Point, cost: int):
        shift = Point(self.min_x, row)
        shifted_point = abs(p - shift)

        costs[shifted_point.y][shifted_point.x] = cost

    def cross_tarp(self, vt):
        intersected = []
        for t in self.tarps:
            if t.intersect(vt):
                intersected.append(t)

        return intersected

    def tarps_box(self):
        min_x, min_y, max_x, max_y = self.start, Vineyard.MAX_Y, self.end, 0,

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
