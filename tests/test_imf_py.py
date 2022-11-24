import unittest
from imf_py import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        ifs = IFS()
        self.assertEqual(ifs.start_date, "2000-01-01")  # add assertion here


if __name__ == '__main__':
    unittest.main()