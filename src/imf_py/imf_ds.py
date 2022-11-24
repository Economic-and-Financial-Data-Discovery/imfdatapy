"""
Authors: Sou-Cheng Choi and Irina Klein, Illinois Institute of Technology
Updated Date: Nov 6, 2022
Creation Date: Jun 15, 2022
"""


import requests

import pandas as pd


def ifs_get_data(search_terms=["Gross Domestic Product, Real"], countries=["US", "DE"],
                 period='Q', start_time="2000", end_time="2022"):
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    series = 'IFS'

    # searches through series:
    series_meta_df = pd.DataFrame()
    key = 'Dataflow'  # Method with series information
    search_term = series  # Term to find in series names
    series_list = requests.get(f'{url}{key}').json() \
        ['Structure']['Dataflows']['Dataflow']
    # Use dict keys to navigate through results:
    des_list, id_list = [], []
    for s in series_list:
        if search_term in s['Name']['#text']:
            des_list.extend([s['Name']['#text']])
            id_list.extend([s['KeyFamilyRef']['KeyFamilyID']])
            # print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")
    series_meta_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Description', 'ID'])
    series_meta_df = series_meta_df.sort_values("ID")
    print(series_meta_df.head())

    # finds the dimentions in the series. We need the indicators.
    des_list, id_list = [], []
    key = f'DataStructure/{series}'  # Method / series
    dimension_list = requests.get(f'{url}{key}').json() \
        ['Structure']['KeyFamilies']['KeyFamily'] \
        ['Components']['Dimension']
    # finds the indicators by the search words:
    for n, dimension in enumerate(dimension_list):
        des_list.extend([n + 1])
        id_list.extend([dimension['@codelist']])
        # print(f"Dimension {n + 1}: {dimension['@codelist']}")
    dim_meta_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Dimension', 'ID'])
    dim_meta_df = dim_meta_df.sort_values("Dimension")
    print(dim_meta_df.head())

    # finds the indicators by the search words:
    des_list, id_list = [], []
    key = f"CodeList/{dimension_list[2]['@codelist']}"
    code_list = requests.get(f'{url}{key}').json() \
        ['Structure']['CodeLists']['CodeList']['Code']
    for code in code_list:
        for search_term in search_terms:
            bool_search_found = search_term in code['Description']['#text']
            if bool_search_found:
                des_list.extend([code['Description']['#text']])
                id_list.extend([code['@value']])

    code_meta_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Description', 'ID'])
    code_meta_df = code_meta_df.sort_values("Description")

    print(code_meta_df.head())

    ##############################################################################
    # get data
    ##############################################################################
    base = f'{url}CompactData/{series}/'
    time = f'?startPeriod={start_time}&endPeriod={end_time}'
    df = pd.DataFrame()

    # sometimes a big list of country codes results in an error, try splitting it into 2 lists and running this and next cell twice.

    dcn_sa = list(code_meta_df["ID"].values)

    temp = pd.DataFrame()
    for cont in countries:
        # print("Current country", cont)
        url = f"{base}{period}.{cont}.{'+'.join(dcn_sa)}.{time}"
        # url = f"{base}{period}..{'+'.join(dcn_sa)}.{time}"
        # print('url',url)
        rq = requests.get(url)
        # print('rq',rq)
        if rq.status_code == 200:
            try:
                response = rq.json()
                series = response['CompactData']['DataSet']['Series']
                N = len(series)
                for n in range(0, N):
                    temp_dic = series[n].get('Obs')

                    temp_df = pd.DataFrame.from_dict(
                        temp_dic
                    ).rename(
                        columns={
                            '@OBS_VALUE': 'Value',
                            '@OBS_STATUS': 'Status'
                        }
                    )
                    temp_df['Country'] = series[n].get('@REF_AREA')
                    temp_df['ID'] = series[n].get('@INDICATOR')
                    temp_df['Period'] = pd.to_datetime(
                        [row.replace('-', '') for row in temp_df['@TIME_PERIOD']]
                    )
                    temp_df.drop('@TIME_PERIOD', axis=1, inplace=True)

                    temp = pd.concat([temp, temp_df], axis=0)
            except:
                print(url)
                pass

    df = pd.concat([temp, df], axis=0)

    df = pd.merge(df, code_meta_df, on="ID", how="left")
    df = df[["Description", "Country", 'Period', "Value", "ID"]]
    # sorting
    df.sort_values(by=["ID", "Country", 'Period'], axis=0, inplace=True)

    # output to csv file
    st_str = "_".join(search_terms)
    ctry_str = "_".join(countries)
    import os
    print(os.getcwd())
    df.to_csv(f"../../out/{st_str}_{ctry_str}_{period}_{start_time}_{end_time}.csv", index=False)

    return df


if __name__ == '__main__':
    df = ifs_get_data(search_terms=["Gross Domestic Product, Real"], countries=["US", "DE"],
                      period='Q', start_time="2000", end_time="2022")