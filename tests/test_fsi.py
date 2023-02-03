import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_fsi_eg1(self):
        fsi = FSI(search_terms=["Value of large exposures"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = fsi.download_data()
        self.assertGreaterEqual(df.shape[0], 146)
        meta_df = fsi.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 6)