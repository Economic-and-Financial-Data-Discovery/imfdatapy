import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        ifs = IFS()
        self.assertEqual(ifs.start_date, None)

if __name__ == '__main__':
    unittest.main()