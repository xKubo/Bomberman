from gamemap import *
import unittest
from timequeue import TimeQueue

class TestTimeObject(unittest.TestCase):
    def test_empty_returns_nothing(self):
        q = TimeQueue()
        items = q.GetOlderOrEqual(0)
        self.assertEqual(len(items), 0)

    def test_return_one_old(self):
        q = TimeQueue()
        to = (2, None)
        q.AddTimeObject(*to)
        items = q.GetOlderOrEqual(1)
        self.assertEqual(items, [])
        items = q.GetOlderOrEqual(3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items, [to])

    def test_return_one_at_a_time(self):
        q = TimeQueue()
        q.AddTimeObject(1, None)
        q.AddTimeObject(2, None)
        items = q.GetOlderOrEqual(0)
        self.assertEqual(items, [])
        items = q.GetOlderOrEqual(1)
        self.assertEqual(items, [(1,None)])
        items = q.GetOlderOrEqual(2)
        self.assertEqual(items, [(2,None)])

if __name__ == '__main__':
    unittest.main()