import unittest
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard


class TestTarp(unittest.TestCase):
    def test_iterative_punctures(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(2, 5))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        v = Vineyard(3, 5, [t0, t1, t2])
        v.plot()

        # Action
        minimum_punctures = v.iterative_punctures()

        # Assert
        self.assertEqual(minimum_punctures, 1)
