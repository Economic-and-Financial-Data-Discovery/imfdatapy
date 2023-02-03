# Bulk download using **imf_data_py**


```python
from imfdatapy.imf import *
```

    2023-02-03 17:37:55,360 imf_log.py:39 - INFO - Current directory /Users/terrya/Documents/ProgramData/imfdatapy/demo
    2023-02-03 17:37:55,360 imf_log.py:40 - INFO - Started log ../log/imfdatapy_2023-02-03-17-37-55.log



```python
ifs = IFS(search_terms=["NGDP_R_SA_XDC"], countries=None, period='Q')
df = ifs.download_data()
print(df.head)
print(df.shape)
```

    2023-02-03 17:37:55,363 imf.py:59 - INFO - Inputs: series = 'IFS', search_terms = ['NGDP_R_SA_XDC']
    2023-02-03 17:38:01,740 imf.py:139 - INFO - Output all IMF series in a (259, 11) table to ../out/series_imf.csv
    2023-02-03 17:38:01,748 imf.py:141 - INFO - Output series containing 'IFS' in a (49, 11) table to ../out/series_ifs.csv



```python
ifs = IFS(search_terms=None, countries=["US"], period='Q')
df = ifs.download_data()
print(df.head)
print(df.shape)
```
