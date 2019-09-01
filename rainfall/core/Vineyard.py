import matplotlib.pyplot as plt
from typing import List
from rainfall.core.Tarp import Tarp


class Vineyard(object):
    __slots__ = ["start", "end", "tarps"]

    def __init__(self, start: int, end: int, tarps: List[Tarp]):
        self.start = start
        self.end = end
        self.tarps = tarps

    def __str__(self):
        tarps = ", ".join([str(t) for t in self.tarps])
        return str.format("<{}, {}> : [{}]", self.start, self.end, tarps)

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
