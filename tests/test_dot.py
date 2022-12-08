import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_dot_eg1(self):
        dot = DOT(search_terms=["trade"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = dot.download_data()
        self.assertGreaterEqual(df.shape[0], 3885)
        meta_df = dot.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 1)


if __name__ == '__main__':
    unittest.main()