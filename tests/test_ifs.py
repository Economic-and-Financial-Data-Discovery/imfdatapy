# The IMF class is a wrapper for the IMF's Data API
# The IMF class is a wrapper for the IMF's Data API
# The IMF class is a wrapper for the IMF's Data API
import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_oo(self):
        ifs = IMF()
        self.assertEqual(ifs.start_date, None)

    def test_imf_ifs_eg1(self):
        ifs = IMF(search_terms=["gross domestic product, real"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)


    def test_imf_ifs_eg2(self):
        ifs = IMF(search_terms=["gross Domestic Product, Real"], countries=["CA", "RU"],
                  period='Q', start_date="1970", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 361)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)


    def test_imf_ifs_eg3(self):
        ifs = IMF(countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)


    def test_imf_ifs_eg4(self):
        ifs = IFS(countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)

    def test_imf_ifs_eg5(self):
        ifs = IFS(countries=["US"], period='Q', start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 5)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

if __name__ == '__main__':
    unittest.main()