from unittest import TestCase

from aoc import Interval

class TestInterval(TestCase):
    def test_len(self):
        self.assertEqual(len(Interval(1, 3)), 2)

    def test_intersect(self):
        a = Interval(1, 3)
        b = Interval(2, 4)
        c = Interval(3, 5)

        self.assertEqual(a.intersect(b), Interval(2, 3))
        self.assertEqual(b.intersect(a), Interval(2, 3))
        self.assertIsNone(a.intersect(c))
        self.assertIsNone(c.intersect(a))