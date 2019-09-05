import unittest
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard


class TestTarp(unittest.TestCase):
    def test_intersecting_perpendicular(self):
        # Assume
        t1 = Tarp(Point(0, 0), Point(1, 1))
        t2 = Tarp(Point(1, 0), Point(0, 1))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertTrue(intersect)

    def test_non_intersecting_perpendicular(self):
        # Assume
        t1 = Tarp(Point(0, 0), Point(1, 1))
        t2 = Tarp(Point(2, 0), Point(1, 1))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertFalse(intersect)

    def test_non_intersecting_parallel(self):
        # Assume
        t1 = Tarp(Point(0, 0), Point(1, 1))
        t2 = Tarp(Point(1, 0), Point(2, 1))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertFalse(intersect)

    def test_intersecting_vertical_slanted(self):
        # Assume
        t1 = Tarp(Point(3, 3), Point(3, 4))
        t2 = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertTrue(intersect)

    def test_non_intersecting_vertical_slanted(self):
        # Assume
        t1 = Tarp(Point(4, 4), Point(4, 5))
        t2 = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertFalse(intersect)

    def test_non_intersecting_vertical_slanted2(self):
        # Assume
        t1 = Tarp(Point(4, 3), Point(4, 4))
        t2 = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t1.intersect(t2)

        # Assert
        self.assertFalse(intersect)
