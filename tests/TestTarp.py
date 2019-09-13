import unittest
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard


class TestTarp(unittest.TestCase):
    def test_intersecting_perpendicular(self):
        # Assume
        vt = Tarp(Point(0, 0), Point(1, 1))
        t = Tarp(Point(1, 0), Point(0, 1))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertTrue(intersect)

    def test_non_intersecting_perpendicular(self):
        # Assume
        vt = Tarp(Point(0, 0), Point(1, 1))
        t = Tarp(Point(2, 0), Point(1, 1))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertFalse(intersect)

    def test_non_intersecting_parallel(self):
        # Assume
        vt = Tarp(Point(0, 0), Point(1, 1))
        t = Tarp(Point(1, 0), Point(2, 1))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertFalse(intersect)

    def test_vertical_intersecting_slanted(self):
        # Assume
        vt = Tarp(Point(3, 3), Point(3, 4))
        t = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertTrue(intersect)

    def test_vertical_intersecting_negative_slanted(self):
        # Assume
        vt = Tarp(Point(3, 2), Point(3, 3))
        t = Tarp(Point(5, 1), Point(2, 3))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertTrue(intersect)

    def test_vertical_non_intersecting_negative_slanted2(self):
        # Assume
        vt = Tarp(Point(10, 11), Point(10, 12))
        t = Tarp(Point(25, 5), Point(0, 15))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertFalse(intersect)

    def test_vertical_intersecting_negative_slanted3(self):
        # Assume
        vt = Tarp(Point(10, 10), Point(10, 11))
        t = Tarp(Point(25, 5), Point(0, 15))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertTrue(intersect)

    def test_vertical_non_intersecting_slanted(self):
        # Assume
        vt = Tarp(Point(4, 4), Point(4, 5))
        t = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertFalse(intersect)

    def test_vertical_non_intersecting_slanted2(self):
        # Assume
        vt = Tarp(Point(4, 3), Point(4, 4))
        t = Tarp(Point(1, 2), Point(4, 4))

        # Action
        intersect = t.intersect(vt)

        # Assert
        self.assertFalse(intersect)
