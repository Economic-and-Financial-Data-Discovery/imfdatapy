import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_hpdd_eg1(self):
        hpdd = HPDD(search_terms=["GDP"], countries=["US"], period='A', start_date=None,
                  end_date=None)
        df = hpdd.download_data()
        self.assertGreaterEqual(df.shape[0], 213)
        meta_df = hpdd.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 1)


if __name__ == '__main__':
    unittest.main()