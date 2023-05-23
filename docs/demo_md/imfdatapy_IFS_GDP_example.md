# Extraction of International Financial Statistics data from the IMF

The example below retrieves quarterly (period: Q) Seasonally Adjusted Real Gross Domestic Product (indicator: NGDP_R_SA_XDC) for the USA (country code: US), from the International Financial Statistics (IFS) series using the **IMFDataPy** package. The function call returns the observation values, and the time period for each value (in the format YYYY-MM-DD).

First, we begin with loading the **IMFDataPy** library for data extraction and from the IMF and **pandas** for data manipulation.

##  `**IMFDataPy**` package 

Source code foris available on [Github](https://github.com/Economic-and-Financial-Data-Discovery/imfdatapy).

The package can be installed using ```pip```.
!pip install imfdatapy

```python
from imfdatapy.imf import *
```


```python
import pandas as pd # for QoQ change calculation
```

To download the data from the International Financial Statistics, we use the ```IFS``` class, provding the search terms for the index we are looking for, the country code, the period frequency (Q) and the period. Use the ```download_data``` method to download the data and the metadata to '../out' folder and create a pandas dataframe. The log messages specify which files are created in the '../out' directory.


```python
pd.options.display.max_colwidth = 90
```


```python
ifs = IFS(search_terms=["gross domestic product"], countries=["US"], period='Q', start_date="2010",
                  end_date="2023")
df = ifs.download_data()
df
```

    2022-12-01 00:10:26,551 imf.py:117 - INFO - Output all IMF series table to ../out/series_imf.csv
    2022-12-01 00:10:26,569 imf.py:119 - INFO - Output series containing 'IFS' table to ../out/series_ifs.csv
    2022-12-01 00:10:39,190 imf.py:249 - WARNING - Failed to download CL_FREQ.
    2022-12-01 00:10:39,770 imf.py:132 - INFO - Output dimension CL_AREA_IFS table to ../out/dim_cl_area_ifs.csv
    2022-12-01 00:10:39,784 imf.py:132 - INFO - Output dimension CL_INDICATOR_IFS table to ../out/dim_cl_indicator_ifs.csv
    2022-12-01 00:10:40,153 imf.py:149 - INFO - Output meta data of IFS table to ../out/meta_ifs.csv
    2022-12-01 00:10:40,172 imf.py:151 - INFO - Output meta data of IFS containing 'gross domestic product' table to ../out/meta_gross domestic product_US_Q_2010_2023.csv
    2022-12-01 00:10:40,482 imf.py:171 - INFO - Output data of IFS containing 'gross domestic product' table to ../out/data_gross domestic product_US_Q_2010_2023.csv






  <div id="df-beed8f22-19d1-48ce-94f1-44112fd49b9f">
    <div class="colab-df-container">
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
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
      <td>US</td>
      <td>2010-01-01</td>
      <td>99.3392105021347</td>
      <td>NGDP_D_SA_IX</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
      <td>US</td>
      <td>2010-04-01</td>
      <td>99.8236914454449</td>
      <td>NGDP_D_SA_IX</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
      <td>US</td>
      <td>2010-07-01</td>
      <td>100.125182516395</td>
      <td>NGDP_D_SA_IX</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
      <td>US</td>
      <td>2010-10-01</td>
      <td>100.711915536026</td>
      <td>NGDP_D_SA_IX</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
      <td>US</td>
      <td>2011-01-01</td>
      <td>101.231913593634</td>
      <td>NGDP_D_SA_IX</td>
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
      <th>97</th>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2021-07-01</td>
      <td>5887605</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>98</th>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2021-10-01</td>
      <td>6087280.3</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>99</th>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-01-01</td>
      <td>6185120</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>100</th>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-04-01</td>
      <td>6312119</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-07-01</td>
      <td>6415822.3</td>
      <td>NGDP_SA_XDC</td>
    </tr>
  </tbody>
</table>
<p>255 rows × 5 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-beed8f22-19d1-48ce-94f1-44112fd49b9f')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-beed8f22-19d1-48ce-94f1-44112fd49b9f button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-beed8f22-19d1-48ce-94f1-44112fd49b9f');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>




Here, all the data that matched the search term is loaded. To view the index names, use the meta data file as shown below.


```python
meta = pd.read_csv('../out/meta_gross domestic product_US_Q_2010_2023.csv')
```


```python
meta
```





  <div id="df-6e4d3215-86e4-42cf-ae20-dc99625e5931">
    <div class="colab-df-container">
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
      <th>ID</th>
      <th>Description.@xml:lang</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NGDP_D_IX</td>
      <td>en</td>
      <td>Gross Domestic Product, Deflator, Index</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NGDP_D_SA_IX</td>
      <td>en</td>
      <td>Gross Domestic Product, Deflator, Seasonally Adjusted, Index</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NGDP_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Nominal, Domestic Currency</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NGDP_SA_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NGDP_NSA_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Nominal, Unadjusted, Domestic Currency</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NGDP_R_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Real, Domestic Currency</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NGDP_R_SA_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Real, Seasonally Adjusted, Domestic Currency</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NGDP_R_NSA_XDC</td>
      <td>en</td>
      <td>Gross Domestic Product, Real, Unadjusted, Domestic Currency</td>
    </tr>
  </tbody>
</table>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-6e4d3215-86e4-42cf-ae20-dc99625e5931')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-6e4d3215-86e4-42cf-ae20-dc99625e5931 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-6e4d3215-86e4-42cf-ae20-dc99625e5931');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>




We are interested in 	Gross Domestic Product, Real, Seasonally Adjusted, Domestic Currency. We will filter the dataframe to contain only this index.


```python
df = df[df['ID']=='NGDP_SA_XDC'].reset_index()

```


```python
df.tail(n=5)
```





  <div id="df-8591373e-e28e-4bab-bf8e-8ccb702676ff">
    <div class="colab-df-container">
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
      <th>index</th>
      <th>Description</th>
      <th>Country</th>
      <th>Period</th>
      <th>Value</th>
      <th>ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>46</th>
      <td>97</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2021-07-01</td>
      <td>5887605</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>47</th>
      <td>98</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2021-10-01</td>
      <td>6087280.3</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>48</th>
      <td>99</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-01-01</td>
      <td>6185120</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>49</th>
      <td>100</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-04-01</td>
      <td>6312119</td>
      <td>NGDP_SA_XDC</td>
    </tr>
    <tr>
      <th>50</th>
      <td>101</td>
      <td>Gross Domestic Product, Nominal, Seasonally Adjusted, Domestic Currency</td>
      <td>US</td>
      <td>2022-07-01</td>
      <td>6415822.3</td>
      <td>NGDP_SA_XDC</td>
    </tr>
  </tbody>
</table>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-8591373e-e28e-4bab-bf8e-8ccb702676ff')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-8591373e-e28e-4bab-bf8e-8ccb702676ff button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-8591373e-e28e-4bab-bf8e-8ccb702676ff');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>





```python
df['Value'] = pd.to_numeric(df['Value'])
```


```python
df['QoQ'] = df['Value'].pct_change()
```

Now, we may plot the results using **matplotlib**.


```python
import matplotlib.pyplot as plt
```


```python
plt.rcParams.update({'font.size': 15})

t = df['Period']
data1 = df['Value'] * 10**6
data2 = df['QoQ']

labels = [f'Q{int(ts.month/3)+1}\n{ts.year}' if ts.month == 1
          else f'Q{int(ts.month/3)+1}' for ts in t]

fig, ax1 = plt.subplots()

ax1.set_xlabel('Period')
ax1.set_ylabel('Real GDP', color='blue')
ax1.set_xticks(t)
ax1.set_xticklabels(labels);
ax1.plot(t, data1, color='blue')
ax1.tick_params(axis='y', labelcolor='black')

ax2 = ax1.twinx()

ax2.set_ylabel('QoQ change', color='red')
ax2.set_xticks(t)
ax2.set_xticklabels(labels);
ax2.plot(t, data2, '--', color='red')
ax2.tick_params(axis='y', labelcolor='black')

fig.set_size_inches(25.5, 5.5)
plt.title('Real GDP by Quarter in the US')
fig.tight_layout()
plt.show()
```


    
![png](imfdatapy_IFS_GDP_example_files/imfdatapy_IFS_GDP_example_19_0.png)
    



```python

```