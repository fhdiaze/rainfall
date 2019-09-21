import matplotlib.pyplot as plt
from typing import List
from matplotlib.ticker import MultipleLocator
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp


class Vineyard(object):
    MAX_X = 10**9
    MAX_Y = 10**9
    MAX_TARPS = 5 * 10**5
    __slots__ = ["start", "end", "tarps", "min_x", "min_y", "max_x", "max_y", "low_tarp", "high_tarp"]

    def __init__(self, start: int, end: int, tarps: List[Tarp]):
        self.start = start
        self.end = end
        self.tarps = sorted(tarps)
        self.min_x, self.min_y, self.max_x, self.max_y = self.tarps_box()
        self.low_tarp = 0
        self.high_tarp = 0

    def __str__(self):
        tarps = ", ".join([str(t) for t in self.tarps])
        return str.format("<{}, {}> : [{}]", self.start, self.end, tarps)

    def p(self):
        ranges = [(self.start, self.end, 0)]

        for t in self.tarps:
            nr = []
            for r in ranges:
                start_range, end_range, cost_range = r
                start_tarp, end_tarp = sorted((t.lower.x, t.higher.x))

                if start_range <= start_tarp <= end_tarp <= end_range\
                        or end_tarp <= start_range or start_tarp >= end_range:
                    nr.append(r)
                elif start_range <= t.lower.x <= end_range:
                    if t.slope() > 0:
                        nr.append((start_range, end_tarp, cost_range))
                    else:
                        nr.append((start_tarp, end_range, cost_range))
                elif start_tarp < start_range < end_range < end_tarp:
                    if t.slope() > 0:
                        nr.append((start_range, end_tarp, cost_range + 1))
                    else:
                        nr.append((start_tarp, end_range, cost_range + 1))
                else:
                    if t.slope() > 0:
                        nr.append((start_range, end_tarp, cost_range + 1))
                        nr.append((end_tarp, end_range, cost_range))
                    else:
                        nr.append((start_range, start_tarp, cost_range))
                        nr.append((start_tarp, end_range, cost_range + 1))
            ranges = nr
        return min([c if sr <= self.start <= er or sr <= self.end <= er else self.MAX_TARPS for (sr, er, c) in ranges])

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

    def min_punctures(self, x, y):
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

    def memo_punctures(self):
        m = dict()
        punctures = self.punctures(lambda x, y: self.min_punctures_with_memo(m, x, y))

        return punctures

    def min_punctures_with_memo(self, m, x, y):
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
        p = 0

        if self.min_x < self.start < self.end < self.max_x:
            width = self.max_x - self.min_x + 1
            costs = [[-1 for _ in range(width)] for _ in range(2)]

            # Init base values
            for x in range(self.min_x, self.max_x + 1):
                p = Point(x, self.min_y)

                if self.start <= p.x <= self.end:
                    cost = 0
                else:
                    cost = Vineyard.MAX_TARPS

                self.set_cost(costs, self.min_y + 1, p, cost)

            for y in range(self.min_y + 1, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    p = Point(x, y)
                    if self.get_cost(costs, y, p) == -1:
                        self.cost(costs, y, p)

                # Flip costs
                costs[1] = costs[0]
                costs[0] = [-1] * width

            p = min(costs[1][self.start - self.min_x:self.end - self.min_x + 1])

        return p

    def cost(self, costs: List[List[int]], row, p: Point):
        # The point could be over tarps
        vertical_delta = Point(0, 1)
        horizontal_delta = Point(1, 0)
        below_point = p - vertical_delta
        intersected = self.cross_tarp(Tarp(below_point, p))

        if intersected:
            slope = intersected[0].slope()
            next_point = p - horizontal_delta if slope > 0 else p + horizontal_delta
            drill_cost = len(intersected) + self.get_cost(costs, row, below_point)
            slide_cost = self.cost(costs, row, next_point)

            # Choose the best option (drill the tarp or let the rain slide)
            cost = min(drill_cost, slide_cost)
        else:
            cost = self.get_cost(costs, row, below_point)

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
        # TODO Add range to the search
        intersected = []
        i = self.low_tarp

        while i <= self.high_tarp < len(self.tarps):
            t = self.tarps[i]

            if t.intersect(vt):
                intersected.append(t)

            if i == self.low_tarp and t.higher.y <= vt.lower.y:
                self.low_tarp += 1
                self.high_tarp += 1 if self.low_tarp > self.high_tarp else 0

            i += 1

            if self.high_tarp < i < len(self.tarps):
                nt = self.tarps[i]
                if nt.lower.y < vt.higher.y:
                    self.high_tarp += 1

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
        ax = plt.axes()

        line = plt.Line2D([self.start, self.end], [0, 0], 4, color='green')
        plt.gca().add_line(line)

        for tarp in self.tarps:
            xs = [tarp.lower.x, tarp.higher.x]
            ys = [tarp.lower.y, tarp.higher.y]
            line = plt.Line2D(xs, ys, 2, color='black')
            plt.gca().add_line(line)

        # Show the grid lines as dark grey lines
        plt.grid(b=True, which='major', color='#666666', linestyle='-')

        plt.axis('equal')
        plt.show()
