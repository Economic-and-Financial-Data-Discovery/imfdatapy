import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):


    def test_imf_bop_eg1(self):

        bop = BOP(search_terms=["current account, total, credit"], countries=["US"], period='Q',
                  start_date="2000", end_date="2022")
        df = bop.download_data()
        self.assertGreaterEqual(df.shape[0], 90)
        meta_df = bop.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 6)


if __name__ == '__main__':
    unittest.main()