from imfdatapy.imf import *

ifs = IFS(search_terms=["NGDP_R_SA_XDC"], countries=None, period='Q')
df = ifs.download_data()
print(df.head)
print(df.shape)

ifs = IFS(search_terms=None, countries=["US"], period='Q')
df = ifs.download_data()
print(df.head)
print(df.shape)