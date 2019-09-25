import matplotlib.pyplot as plt
from typing import List
from matplotlib.ticker import MultipleLocator
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp


class Vineyard(object):
    MAX_TARPS = 5 * 10 ** 5
    __slots__ = ["start", "end", "tarps"]

    def __init__(self, start: int, end: int, tarps: List[Tarp]):
        """Creates a vineyard

        :param start: Start of the vineyard
        :param end: End of vineyard
        :param tarps: Vineyard's tarps
        """
        self.start = start
        self.end = end
        self.tarps = sorted(tarps)

    def __str__(self):
        """Convert self tarp to its string representation

        :return: Tarp as string
        """
        tarps = ", ".join([str(t) for t in self.tarps])
        return str.format("<{}, {}> : [{}]", self.start, self.end, tarps)

    def punctures(self):
        """Calculates the minimum punctures required to get rain over the vineyard

        :return: The minimum punctures
        """
        ranges = [(self.start, self.end, 0)]

        for t in self.tarps:
            nr = []
            for r in ranges:
                start_range, end_range, cost_range = r
                start_tarp, end_tarp = sorted((t.lower.x, t.higher.x))

                if start_range <= start_tarp <= end_tarp <= end_range \
                        or end_tarp < start_range or start_tarp > end_range:
                    nr.append(r)
                elif start_range <= t.lower.x <= end_range:
                    if t.slope() > 0:
                        nr.append((start_range, end_tarp, cost_range))
                    else:
                        nr.append((start_tarp, end_range, cost_range))
                elif start_tarp < start_range < end_range < end_tarp:
                    if t.slope() > 0:
                        nr.append((start_range, end_range, cost_range + 1))
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

        punctures = [c if sr <= self.end and self.start <= er else self.MAX_TARPS for (sr, er, c) in ranges]

        return min(punctures)

    def plot(self):
        """Plots the vineyard

        """
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
