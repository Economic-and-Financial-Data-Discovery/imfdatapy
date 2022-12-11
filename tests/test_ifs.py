# The IMF class is a wrapper for the IMF's Data API
import unittest
from imfdatapy.imf import *

class MyTestCase(unittest.TestCase):

    def test_imf_oo(self):
        ifs = IFS()
        self.assertEqual(ifs.start_date, None)

    def test_imf_ifs_eg1(self):
        ifs = IFS(search_terms=["gross domestic product, real"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)


    def test_imf_ifs_eg2(self):
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["CA", "RU"],
                  period='Q', start_date="1970", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 361)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)


    def test_imf_ifs_eg3(self):
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)


    def test_imf_ifs_eg4(self):
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period='Q', start_date="2000", end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)

    def test_imf_ifs_eg5(self):
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period='Q', start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg6(self):
        # test for invalid period input
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period=None, start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 72)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg7(self):
        # test for invalid country ID
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["XX", "US"], period="Q", start_date=None, end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg8(self):
        # test for invalid start_date
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period="Q", start_date="20", end_date=None)
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 374)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg9(self):
        # test for invalid end_date
        ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["US"], period=None, start_date=None, end_date="XY")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 72)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg10(self):
        # test for invalid series code --- give ERROR and stop
        ifs = IFS(series="IFSXTZ", search_terms=["gross Domestic Product, Real"], countries=["US"])
        df = ifs.download_data()
        self.assertIsNone(df)


    def test_imf_ifs_eg11(self):
        # test for search term that does not exist --- give ERROR and stop
        ifs = IFS(search_terms=["XYZ"], countries=["US"])
        df = ifs.download_data()
        self.assertIsNone(df)

    def test_imf_ifs_eg12(self):
        # test for search term with one invalid value is still going to work
        ifs = IFS(search_terms=["XYZ", "gross domestic product, real"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg13(self):
        # test for getting a given IFS code
        ifs = IFS(search_terms=["NGDP_R_SA_XDC"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 91)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 1)
        self.assertGreaterEqual(meta_df.shape[1], 3)

    def test_imf_ifs_eg14(self):
        # test for getting search terms list with more than 1 element
        ifs = IFS(search_terms=["NGDP_R_SA_XDC", "gross Domestic Product, Real"], countries=["US"], period='Q', start_date="2000",  end_date="2022")
        df = ifs.download_data()
        self.assertGreaterEqual(df.shape[0], 174)
        self.assertGreaterEqual(df.shape[1], 10)
        meta_df = ifs.get_meta()
        self.assertGreaterEqual(meta_df.shape[0], 3)
        self.assertGreaterEqual(meta_df.shape[1], 3)


if __name__ == '__main__':
    unittest.main()