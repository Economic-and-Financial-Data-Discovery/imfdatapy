import logging.config
import unittest


from imfdatapy.imf import *


class MyTestCase(unittest.TestCase):

    def test_imf_gfsr_eg1(self):
        gfsr = GFSR(search_terms=["central government"], countries=["US"], period='A', start_date="2000", end_date="2022")
        df = gfsr.download_data()
        self.assertGreaterEqual(df.shape[0], 14784)
        meta_df = gfsr.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 4)




if __name__ == '__main__':
    unittest.main()

"""

"""