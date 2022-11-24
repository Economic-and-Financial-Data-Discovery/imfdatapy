import logging.config
import unittest


from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_oo(self):
        ifs = IMF()
        self.assertEqual(ifs.start_date, "2000-01-01")

    def test_imf_ifs_eg1(self):
        ifs = IMF(search_terms=["gross domestic product, real"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)

        tm.sleep(1)

    def test_imf_ifs_eg2(self):
        ifs = IMF(search_terms=["gross Domestic Product, Real"], countries=["CA", "RU"],
                  period='Q', start_date="1970", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 361)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        tm.sleep(1)

    def test_imf_ifs_eg3(self):
        ifs = IMF(countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        tm.sleep(1)

    def test_imf_ifs_eg4(self):
        ifs = IFS(countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        tm.sleep(1)


if __name__ == '__main__':
    unittest.main()

"""

"""