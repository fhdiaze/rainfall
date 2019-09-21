import unittest
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard


class TestVineyard(unittest.TestCase):
    def test_punctures(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(2, 5))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        v = Vineyard(3, 5, [t0, t1, t2])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(1, minimum_punctures)

    def test_punctures1(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(2, 5))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        v = Vineyard(4, 6, [t0, t1, t2])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(0, minimum_punctures)

    def test_punctures2(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(1, 6))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        v = Vineyard(2, 3, [t0, t1, t2])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(3, minimum_punctures)

    def test_punctures3(self):
        # Assume
        t0 = Tarp(Point(32, 50), Point(12, 60))
        t1 = Tarp(Point(30, 60), Point(8, 70))
        t2 = Tarp(Point(25, 70), Point(0, 80))
        t3 = Tarp(Point(15, 30), Point(28, 40))
        t4 = Tarp(Point(5, 20), Point(14, 25))
        v = Vineyard(10, 20, [t0, t1, t2, t3, t4])
        v.plot()

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(2, minimum_punctures)

    def test_punctures4(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(1, 6))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        v = Vineyard(5, 7, [t0, t1, t2])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(0, minimum_punctures)

    def test_punctures5(self):
        # Assume
        t0 = Tarp(Point(8, 2), Point(5, 3))
        t1 = Tarp(Point(10, 2), Point(5, 6))
        t2 = Tarp(Point(9, 2), Point(4, 4))
        v = Vineyard(2, 3, [t0, t1, t2])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(0, minimum_punctures)

    def test_punctures6(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 2), Point(1, 6))
        t2 = Tarp(Point(5, 2), Point(0, 4))
        t3 = Tarp(Point(3, 1), Point(7, 2))
        v = Vineyard(2, 3, [t0, t1, t2, t3])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(0, minimum_punctures)

    def test_punctures7(self):
        # Assume
        t0 = Tarp(Point(4, 2), Point(1, 3))
        t1 = Tarp(Point(6, 1), Point(1, 4))
        v = Vineyard(3, 4, [t0, t1])

        # Action
        minimum_punctures = v.p()

        # Assert
        self.assertEqual(1, minimum_punctures)
