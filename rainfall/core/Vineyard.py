import matplotlib.pyplot as plt
from typing import List
from rainfall.core.Store import Store
from rainfall.core.Tarp import Tarp


class Vineyard(object):
    __slots__ = ["start", "end", "tarps", "store"]

    def __init__(self, start: int, end: int, tarps: List[Tarp], max_x: int = None):
        """Creates a vineyard

        :param start: Start of the vineyard
        :param end: End of vineyard
        :param tarps: Vineyard's tarps
        """
        self.start = start
        self.end = end
        self.tarps = sorted(tarps)
        if max_x is None:
            xs = list(map(lambda t: max(t.lower.x, t.higher.x), tarps))
            xs.append(end)
            max_x = max(xs)
        self.store = Store(self.start, self.end, max_x)

    def __str__(self):
        """Converts self vineyard to its string representation

        :return: Vineyard as string
        """
        tarps = ", ".join([str(t) for t in self.tarps])
        return str.format("<{}, {}> : [{}]", self.start, self.end, tarps)

    def punctures(self):
        """Calculates the minimum punctures required to get rain over the vineyard

        :return: The minimum punctures
        """

        for t in self.tarps:
            self.store.update(t)

        return self.store.min_punctures(self.start, self.end)

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
