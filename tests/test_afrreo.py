import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):


    def test_imf_afrreo_eg1(self):
        affreo = AFRREO(search_terms=["total expenditure"], countries=["CF"], period='A', start_date=None, end_date=None)
        df = affreo.download_data()
        self.assertGreaterEqual(df.shape[0], 20)
        meta_df = affreo.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 1)


if __name__ == '__main__':
    unittest.main()