import unittest
from imfdatapy.imf import *


class MyTestCase(unittest.TestCase):

    def test_imf_ifs_eg1(self):
        ifs = IFS(search_terms=["gross"], countries=["US"], period='A', start_date="2020",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)


if __name__ == '__main__':
    unittest.main()