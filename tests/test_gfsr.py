import unittest
from imfdatapy.imf import *

class TestGFSR(unittest.TestCase):

    def test_imf_gfsr_eg1(self):
        gfsr = GFSR(search_terms=["social contributions"], countries=["US"], period='A', start_date="2000", end_date="2022")
        df = gfsr.download_data()
        self.assertGreaterEqual(df.shape[0], 2464)
        meta_df = gfsr.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 7)

    def test_imf_gfsr_eg2(self):
        # correct for invalid input period
        gfsr = GFSR(search_terms=["central government"], countries=["US"], period='A', start_date="2000", end_date="2022")
        df = gfsr.download_data()
        self.assertIsNone(df)


if __name__ == '__main__':
    unittest.main()