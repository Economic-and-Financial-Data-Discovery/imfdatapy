# The IMF class is a wrapper for the IMF's Data API
import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_eg1(self):
        # test for getting all countries for a given IFS code
        ifs = IFS(search_terms=["NGDP_R_SA_XDC"], countries=None, period="Q", start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_eg1(self):
        # test for getting all countries for a given IFS code
        ifs = IFS(search_terms=None, countries=["US"], period="Q", start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)


if __name__ == '__main__':
    unittest.main()