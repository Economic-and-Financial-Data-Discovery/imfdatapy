# imfdatapy_demo


```python
from imfdatapy.imf import *
```


```python
ifs = IFS(search_terms=["gross domestic product, real"], countries=["US"], period='Q', start_date="2000",
                  end_date="2022")
df = ifs.download_data()
df
```

    2022-11-25 02:01:42,761 - root - INFO - countries_str = 'US', self.start_date = '2000', self.end_date = '2022'
    2022-11-25 02:01:43,334 - root - INFO - Output all IMF series table to ../out/series_imf.csv
    2022-11-25 02:01:43,365 - root - INFO - Output series containing 'IFS' table to ../out/series_ifs.csv
    2022-11-25 02:02:07,999 - root - WARNING - Failed to download CL_FREQ.
    2022-11-25 02:02:08,736 - root - INFO - Output dimension CL_AREA_IFS table to ../out/dim_cl_area_ifs.csv
    2022-11-25 02:02:08,750 - root - INFO - Output dimension CL_INDICATOR_IFS table to ../out/dim_cl_indicator_ifs.csv
    2022-11-25 02:02:09,235 - root - INFO - Output meta data of IFS table to ../out/meta_ifs.csv
    2022-11-25 02:02:09,249 - root - INFO - self.meta_df.shape = (3, 3)
    2022-11-25 02:02:09,250 - root - INFO - Output meta data of IFS containing 'gross domestic product, real' table to ../out/meta_gross domestic product, real_US_Q_2000_2022.csv
    2022-11-25 02:03:00,718 - root - INFO - self.data_df.shape = (174, 5)
    2022-11-25 02:03:00,722 - root - INFO - Output data of IFS containing 'gross domestic product, real' table to ../out/data_gross domestic product, real_US_Q_2000_2022.csv





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Description</th>
      <th>Country</th>
      <th>Period</th>
      <th>Value</th>
      <th>ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>US</td>
      <td>2002-01-01</td>
      <td>3263869</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>US</td>
      <td>2002-04-01</td>
      <td>3362508</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>US</td>
      <td>2002-07-01</td>
      <td>3401820</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>US</td>
      <td>2002-10-01</td>
      <td>3460159</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>US</td>
      <td>2003-01-01</td>
      <td>3340163</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>169</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>US</td>
      <td>2021-07-01</td>
      <td>4918148.5</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>170</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>US</td>
      <td>2021-10-01</td>
      <td>5001545.3</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>171</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>US</td>
      <td>2022-01-01</td>
      <td>4981022</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>172</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>US</td>
      <td>2022-04-01</td>
      <td>4973817.8</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>173</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>US</td>
      <td>2022-07-01</td>
      <td>5005430.3</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
  </tbody>
</table>
<p>174 rows × 5 columns</p>
</div>




```python
ifs.describe_data()
```


```python
ifs = IFS(search_terms=["gross Domestic Product, Real"], countries=["CA", "RU"],
                  period='Q',  start_date="1970", end_date="2022")
df = ifs.download_data()
df
```

    2022-11-25 02:03:15,465 - root - INFO - countries_str = 'CA, RU', self.start_date = '1970', self.end_date = '2022'
    2022-11-25 02:03:16,065 - root - INFO - Output all IMF series table to ../out/series_imf.csv
    2022-11-25 02:03:16,097 - root - INFO - Output series containing 'IFS' table to ../out/series_ifs.csv
    2022-11-25 02:03:32,074 - root - WARNING - Failed to download CL_FREQ.
    2022-11-25 02:03:32,756 - root - INFO - Output dimension CL_AREA_IFS table to ../out/dim_cl_area_ifs.csv
    2022-11-25 02:03:32,769 - root - INFO - Output dimension CL_INDICATOR_IFS table to ../out/dim_cl_indicator_ifs.csv
    2022-11-25 02:03:33,126 - root - INFO - Output meta data of IFS table to ../out/meta_ifs.csv
    2022-11-25 02:03:33,141 - root - INFO - self.meta_df.shape = (3, 3)
    2022-11-25 02:03:33,143 - root - INFO - Output meta data of IFS containing 'gross Domestic Product, Real' table to ../out/meta_gross Domestic Product, Real_CA_RU_Q_1970_2022.csv
    2022-11-25 02:04:33,893 - root - INFO - self.data_df.shape = (361, 5)
    2022-11-25 02:04:33,904 - root - INFO - Output data of IFS containing 'gross Domestic Product, Real' table to ../out/data_gross Domestic Product, Real_CA_RU_Q_1970_2022.csv





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Description</th>
      <th>Country</th>
      <th>Period</th>
      <th>Value</th>
      <th>ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>286</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>RU</td>
      <td>2003-01-01</td>
      <td>12950180.3</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>287</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>RU</td>
      <td>2003-04-01</td>
      <td>13906392.6</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>288</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>RU</td>
      <td>2003-07-01</td>
      <td>15267819.4</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>289</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>RU</td>
      <td>2003-10-01</td>
      <td>15661990.5</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>290</th>
      <td>Gross Domestic Product, Real, Unadjusted, Dome...</td>
      <td>RU</td>
      <td>2004-01-01</td>
      <td>13887920.9</td>
      <td>NGDP_R_NSA_XDC</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>281</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>RU</td>
      <td>2020-07-01</td>
      <td>22253279.9</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>282</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>RU</td>
      <td>2020-10-01</td>
      <td>22417897</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>283</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>RU</td>
      <td>2021-01-01</td>
      <td>22570515.7</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>284</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>RU</td>
      <td>2021-04-01</td>
      <td>23290725.9</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
    <tr>
      <th>285</th>
      <td>Gross Domestic Product, Real, Seasonally Adjus...</td>
      <td>RU</td>
      <td>2021-07-01</td>
      <td>23105679.7</td>
      <td>NGDP_R_SA_XDC</td>
    </tr>
  </tbody>
</table>
<p>361 rows × 5 columns</p>
</div>




```python
bop = BOP(search_terms=["current account, total, credit"], countries=["US"], period='Q',
                  start_date="2000", end_date="2022")
df = bop.download_data()
```

    2022-11-25 02:07:43,545 - root - INFO - countries_str = 'US', self.start_date = '2000', self.end_date = '2022'
    2022-11-25 02:07:44,079 - root - INFO - Output all IMF series table to ../out/series_imf.csv
    2022-11-25 02:07:44,108 - root - INFO - Output series containing 'BOP' table to ../out/series_bop.csv
    2022-11-25 02:08:10,200 - root - WARNING - Failed to download CL_FREQ.
    2022-11-25 02:08:12,137 - root - INFO - Output dimension CL_AREA_BOP table to ../out/dim_cl_area_bop.csv
    2022-11-25 02:08:12,169 - root - INFO - Output dimension CL_INDICATOR_BOP table to ../out/dim_cl_indicator_bop.csv
    2022-11-25 02:08:13,664 - root - INFO - Output meta data of BOP table to ../out/meta_bop.csv
    2022-11-25 02:08:13,680 - root - INFO - self.meta_df.shape = (6, 3)
    2022-11-25 02:08:13,682 - root - INFO - Output meta data of BOP containing 'current account, total, credit' table to ../out/meta_current account, total, credit_US_Q_2000_2022.csv
    2022-11-25 02:08:43,021 - root - INFO - self.data_df.shape = (90, 5)
    2022-11-25 02:08:43,026 - root - INFO - Output data of BOP containing 'current account, total, credit' table to ../out/data_current account, total, credit_US_Q_2000_2022.csv



```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Description</th>
      <th>Country</th>
      <th>Period</th>
      <th>Value</th>
      <th>ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2000-01-01</td>
      <td>353383</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2000-04-01</td>
      <td>374019</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2000-07-01</td>
      <td>375897</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2000-10-01</td>
      <td>382816</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2001-01-01</td>
      <td>362875</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>85</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2021-04-01</td>
      <td>930309</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>86</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2021-07-01</td>
      <td>946612</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>87</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2021-10-01</td>
      <td>1021657</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>88</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2022-01-01</td>
      <td>1005348</td>
      <td>BXCA_BP6_USD</td>
    </tr>
    <tr>
      <th>89</th>
      <td>Current Account, Total, Credit, US Dollars</td>
      <td>US</td>
      <td>2022-04-01</td>
      <td>1106396</td>
      <td>BXCA_BP6_USD</td>
    </tr>
  </tbody>
</table>
<p>90 rows × 5 columns</p>
</div>




```python
ifs = IFS(series="DOT", search_terms=["trade"], countries=["US"], period='Q', start_date="2000",
          end_date="2022")
df = ifs.download_data()
df
```


```python
ifs = IFS(series="BOP", search_terms=["current account, total, credit"], countries=["US"], period='Q',
      start_date="2000", end_date="2022")
df = ifs.download_data()
df
```


```python
ifs = IFS(series="GFSR", search_terms=["central government"], countries=["US"], period='A', start_date="2000", end_date="2022")
df = ifs.download_data()
df
```


```python
ifs = IFS(series="FSI", search_terms=["Value of large exposures"], countries=["US"], period='A', start_date="2000", end_date="2022")
df = ifs.download_data()
df
```
