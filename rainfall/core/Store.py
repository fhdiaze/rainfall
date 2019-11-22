from rainfall.core.Tarp import Tarp


class Store:
    MAX_TARPS = 5 * 10 ** 5
    MAX_X = 10 ** 9
    __slots__ = ["punctures"]

    def __init__(self, l: int, r: int):
        self.punctures = [Store.MAX_TARPS] * Store.MAX_X
        self.punctures[l:r + 1] = 0

    def update(self, t: Tarp):
        xl, xr = t.sorted_xs()

        if t.slope() > 0:
            i = xl + 1
            delta = 1
        else:
            i = xr - 1
            delta = -1

        for x in range(xr - xl):
            self.punctures[i] = min(self.punctures[i] + 1, self.punctures[i + delta])

    def min_punctures(self, xi: int, xf: int):
        return min(self.punctures[xi, xf + 1])
