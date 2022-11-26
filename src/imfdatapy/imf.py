"""
Authors: Sou-Cheng Choi and Irina Klein, Illinois Institute of Technology
Updated Date: Nov 24, 2022
Creation Date: Jun 15, 2022
"""
from abc import ABC, abstractmethod

from os import path
from os import mkdir

import time as tm

import pandas as pd

import logging
import logging.config
import requests
import itertools

# Create logger TODO add filename and line number
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='../../log/imf.log', encoding='utf-8', level=logging.info)


# abstract class
class Series(ABC):

    def __init__(self, series='IFS', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        """

        :param series: IMF series name, e.g., "IFS", "DOT"
        :param search_terms: list of strings to find in indicator names in the series
        :param countries: list of strings containing ISO-2 code of country names
        :param period: frequency of time series
        :param start_date: start date of time series
        :param end_date: end date of time series
        """
        self.series = series
        self.search_terms = ["Gross Domestic Product, Real"] if search_terms is None else search_terms
        self.countries = ["US"] if countries is None else countries
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.start_time, self.end_time = start_date[:4], end_date[:4]
        self.url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
        countries_str = ", ".join(self.countries)
       
        #logging.info(f"{countries_str = }, {self.start_date = }, {self.end_date = }")

        self.meta_df = pd.DataFrame()
        self.series_df = pd.DataFrame()
        self.data_df = pd.DataFrame()
        self.dim_dict = {}

        self._max_requests = 10
        self._sleep_sec = 1
        
        # Doesn't create new directory in colab
        outdir = '../out'
        if not path.exists(outdir):
            mkdir(outdir)

    def get_series_names(self):
        """
        TODO
        """
        pass

    @abstractmethod
    def download_meta(self):
        pass

    @abstractmethod
    def download_data(self):
        pass

    @abstractmethod
    def get_meta(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def describe_meta(self):
        pass

    @abstractmethod
    def describe_data(self):
        pass


# concrete class
class IMF(Series):

    def __init__(self, series='IFS', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series, search_terms, countries, period, start_date, end_date)

    def output_series(self, series=None):
        """ Method to output all or some IMF series names to a .csv file in 'out'.

        :param series: Series code as a string

        """
        # output to csv file
        if series is None:
            outfile_path = f"../out/series_imf.csv"
        else:
            outfile_path = f"../out/series_{series.lower()}.csv"
        self.series_df.to_csv(outfile_path, index=False)
        if series is None:
            logging.info(f"Output all IMF series table to {outfile_path}")
        else:
            logging.info(f"Output series containing '{series}' table to {outfile_path}")

    def output_dim(self, dim_name=None):
        """ Method to output all or some dimension tables to a .csv file in 'out'.

        :param dim_name: Dimension name as a string

        """
        # output to csv file
        if dim_name is not None:
            for key in self.dim_dict.keys():
                outfile_path = f"../out/dim_{key.lower()}.csv"
                self.dim_dict[key].to_csv(outfile_path, index=False)
                logging.info(f"Output dimension {key} table to {outfile_path}")

    def output_meta(self, indicator=None):
        """ Method to output all or some indicators in a tables to a .csv file in 'out'.

        :param indicator: Indicator code as a string

        """
        # output to csv file
        if indicator is None:
            outfile_path = f"../out/meta_{self.series.lower()}.csv"
        else:
            st_str = "_".join(self.search_terms)
            ctry_str = "_".join(self.countries)
            outfile_path = f"../out/meta_{st_str}_{ctry_str}_{self.period}_{self.start_time}_{self.end_time}.csv"
        self.meta_df.to_csv(outfile_path, index=False)
        if indicator is None:
            logging.info(f"Output meta data of {self.series} table to {outfile_path}")
        else:
            logging.info(f"Output meta data of {self.series} containing '{st_str}' table to {outfile_path}")

    def output_data(self, data=None):
        """ Method to output downloaded time series data to a .csv file in 'out'.

        :param data: TODO

        """

        # output to csv file
        if data is None:
            outfile_path = f"../out/data_{self.series.lower()}.csv"
        else:
            st_str = "_".join(self.search_terms)
            ctry_str = "_".join(self.countries)
            outfile_path = f"../out/data_{st_str}_{ctry_str}_{self.period}_{self.start_time}_{self.end_time}.csv"
        self.data_df.to_csv(outfile_path, index=False)
        if data is None:
            logging.info(f"Output data of {self.series} table to {outfile_path}")
        else:
            logging.info(f"Output data of {self.series} containing '{st_str}' table to {outfile_path}")

    # overriding abstract methods
    def get_series_names(self):
        """

        :return: relevant IMF series names
        """
        # searches through series:
        key = 'Dataflow'  # Method with series information
        search_terms = self.series  # Term to find in series names
        rq = self.repeat_request(url=f'{self.url}{key}')
        if rq.status_code == 200:
            series_list = rq.json()['Structure']['Dataflows']['Dataflow']
            # find all series names
            self.series_df = pd.json_normalize(series_list)
            self.series_df = self.series_df.sort_values("KeyFamilyRef.KeyFamilyID")
            self.output_series()
        else:
            logging.warning(f"Failed to download series.")

        # Filter series names
        self.series_df["search_found"] = False
        string_columns = self.series_df.select_dtypes(include=object).columns
        for col, search_term in itertools.product(string_columns, [search_terms]):
            #logging.debug(f"{col = }, {search_term = }")
            self.series_df["search_found"] = self.series_df["search_found"] | self.series_df[col].str.lower().str.contains(
                search_term.lower())
            #logging.debug(self.series_df["search_found"].describe())
        self.series_df = self.series_df[self.series_df["search_found"]]
        self.series_df = self.series_df.drop(['search_found'], axis=1)
        self.output_series(series=self.series)
        # Use dict keys to navigate through results:
        """
        des_list, id_list = [], []
        for s in series_list:
            if search_term in s['Name']['#text']:
                des_list.extend([s['Name']['#text']])
                id_list.extend([s['KeyFamilyRef']['KeyFamilyID']])
                # logging.debug(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")
        self.series_names_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Description', 'ID'])
        self.series_names_df = self.series_names_df.sort_values("ID")
        """
        logging.debug(self.series_df.head())
        return self.series_df

    def get_dimensions(self):
        """

        :return: TODO
        """
        # finds the dimensions in the series. We need the indicators.
        des_list, id_list = [], []
        key = f'DataStructure/{self.series}'  # DataStructure Method / series
        rq = self.repeat_request(url=f'{self.url}{key}')
        if rq.status_code == 200:
            dimension_list = rq.json()['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
            self.dim_df = pd.json_normalize(dimension_list)

            # finds the indicators by the search words:
            for n, dimension in enumerate(dimension_list):
                des_list.extend([n + 1])
                id_list.extend([dimension['@codelist']])
                logging.debug(f"Dimension {n + 1}: {dimension['@codelist']}")
            self.dim_meta_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Dimension', 'ID'])
            self.dim_meta_df = self.dim_meta_df.sort_values("Dimension")

            for n in range(0, len(dimension_list)):
                try:
                    dim_name = dimension_list[n]['@codelist']
                    key = f"CodeList/{dim_name}"
                    rq = self.repeat_request(url=f'{self.url}{key}')
                    if rq.status_code == 200:
                        code_list = rq.json()['Structure']['CodeLists']['CodeList']['Code']
                        code_df = pd.json_normalize(code_list)
                        self.dim_dict[dim_name] = code_df
                        logging.debug(f"Dimension {dim_name} details: \n{code_df}")
                    else:
                        logging.warning(f"Failed to download {dim_name}.")
                except:
                    logging.error(f"Cannot extract dimension {dim_name} details.")

            self.output_dim("")
        else:
            logging.warning(f"Failed to download dimensions.")

        return des_list, dimension_list, id_list

    def download_meta(self, des_list, dimension_list, id_list):
        """

        :param des_list:  TODO
        :param dimension_list:
        :param id_list:
        :return: meta data of time series
        """
        # finds the indicators by the search words:
        for n, dimension in enumerate(dimension_list):
            des_list.extend([n + 1])
            id_list.extend([dimension['@codelist']])
            # logging.debug(f"Dimension {n + 1}: {dimension['@codelist']}")
        dim_meta_df = pd.DataFrame(list(zip(des_list, id_list)), columns=['Dimension', 'ID'])
        dim_meta_df = dim_meta_df.sort_values("Dimension")
        logging.debug(dim_meta_df.head())

        # finds the indicators by the search words
        key = f"CodeList/{dimension_list[2]['@codelist']}"
        rq = self.repeat_request(url=f'{self.url}{key}')
        if rq.status_code == 200:
            code_list = rq.json()['Structure']['CodeLists']['CodeList']['Code']
            self.meta_df = pd.json_normalize(code_list)
            self.output_meta()

            self.meta_df["search_found"] = False
            string_columns = self.meta_df.select_dtypes(include=object).columns
            for col, search_term in itertools.product(string_columns, self.search_terms):
                #logging.debug(f"{col = }, {search_term = }")
                self.meta_df["search_found"] = self.meta_df["search_found"] | self.meta_df[
                    col].str.lower().str.contains(
                    search_term.lower())
                logging.debug(self.meta_df["search_found"].describe())
                logging.debug(self.meta_df[self.meta_df["search_found"]])
            self.meta_df = self.meta_df[self.meta_df["search_found"]]
            self.meta_df = self.meta_df.drop(['search_found'], axis=1)

            if "ID" not in self.meta_df.columns:
                self.meta_df.columns = ["ID", *list(self.meta_df.columns)[1:]]
            if "Description" not in self.meta_df.columns:
                self.meta_df.columns = [*list(self.meta_df.columns)[:-1], "Description"]
            #logging.info(f"{self.meta_df.shape = }")
            self.output_meta(indicator="")
        else:
            logging.warning(f"Failed to download meta data.")

        return self.meta_df

    # overriding abstract method
    def download_data(self):
        """

        :return: time series data downloaded
        """
        self.get_series_names()

        des_list, dimension_list, id_list = self.get_dimensions()  # TODO simplify
        self.meta_df = self.download_meta(des_list, dimension_list, id_list)  # TODO simplify

        base = f'{self.url}CompactData/{self.series}/'
        time = f'?startPeriod={self.start_time}&endPeriod={self.end_time}'
        self.data_df = pd.DataFrame()
        # sometimes a big list of country codes results in an error, try splitting it into 2 lists and running this and next cell twice.
        dcn_sa = list(self.meta_df["ID"].values)
        temp = pd.DataFrame()
        for cont in self.countries:

            # logging.debug("Current country", cont)
            url = f"{base}{self.period}.{cont}.{'+'.join(dcn_sa)}.{time}"
            # url = f"{base}{period}..{'+'.join(dcn_sa)}.{time}"
            # logging.debug('url',url)
            rq = self.repeat_request(url)
            # logging.debug('rq',rq)
            if rq.status_code == 200:
                try:
                    response = rq.json()
                    series = response['CompactData']['DataSet']['Series']
                    temp_df = pd.DataFrame()
                    if isinstance(series, dict):
                        if isinstance(series.get("Obs"), list):
                            temp_df = pd.concat([temp_df, pd.json_normalize(series.get("Obs"))])
                        for k in series.keys():
                            if k != "Obs":
                                temp_df[k] = series.get(k)

                        temp_df = temp_df.rename(
                            columns={
                                '@OBS_VALUE': 'Value',
                                '@INDICATOR': 'ID',
                                '@INDICATOR_CODE': 'ID',
                                '@REF_AREA': 'Country'
                            }
                        )
                        temp_df['Period'] = pd.to_datetime(
                            [row.replace('-', '') for row in temp_df['@TIME_PERIOD']]
                        )
                        temp_df.drop('@TIME_PERIOD', axis=1, inplace=True)

                        temp = pd.concat([temp, temp_df], axis=0)
                    elif isinstance(series, list):
                        series_len = len(series)
                        for n in range(0, series_len):
                            temp_dic = series[n].get('Obs')

                            temp_df = pd.DataFrame.from_dict(
                                temp_dic
                            ).rename(
                                columns={
                                    '@OBS_VALUE': 'Value',
                                    '@OBS_STATUS': 'Status'
                                }
                            )

                            # temp_df['Country'] = series[n].get('@REF_AREA')
                            # temp_df['ID'] = series[n].get('@INDICATOR')
                            for k in series[n].keys():
                                if k != "Obs":
                                    temp_df[k] = series[n].get(k)

                            temp_df = temp_df.rename(
                                columns={
                                    '@OBS_VALUE': 'Value',
                                    '@INDICATOR': 'ID',
                                    '@REF_SECTOR': 'ID',  # for GFSR
                                    '@REF_AREA': 'Country'
                                }
                            )
                            temp_df['Period'] = pd.to_datetime(
                                [row.replace('-', '') for row in temp_df['@TIME_PERIOD']]
                            )
                            temp_df.drop('@TIME_PERIOD', axis=1, inplace=True)

                            temp = pd.concat([temp, temp_df], axis=0)
                except:
                    logging.error(url)
                    pass

        self.data_df = pd.concat([temp, self.data_df], axis=0)
        self.data_df = pd.merge(self.data_df, self.meta_df, on="ID", how="left")
        self.data_df = self.data_df[["Description", "Country", 'Period', "Value", "ID"]]
        # sorting
        self.data_df.sort_values(by=["ID", "Country", 'Period'], axis=0, inplace=True)
        #logging.info(f"{self.data_df.shape = }")
        self.output_data(data="")

        return self.data_df

    def repeat_request(self, url):
        rq = None
        for _ in range(self._max_requests):
            rq = requests.get(url)
            if rq.status_code == 200:
                return rq

            tm.sleep(self._sleep_sec)

        return rq

    # overriding abstract method
    def get_meta(self):
        """

        :return: meta data of time series data
        """
        return self.meta_df

    # overriding abstract method
    def get_data(self):
        """

        :return: time series data
        """
        return self.data_df

    def describe_data(self):
        """

        :return: summary of time series data
        """
        # TODO groupby countries summary
        return

    def describe_meta(self):
        """

        :return: summary of meta data
        """

        return self.meta_df.describe(include="all")


class IFS(IMF):
    def __init__(self, series='IFS', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date)


class DOT(IMF):
    def __init__(self, series='DOT', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date)


class BOP(IMF):
    def __init__(self, series='BOP', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date)


class FSI(IMF):
    def __init__(self, series='FSI', search_terms=None, countries=None, period='Q',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date)


class GFSR(IMF):
    """
    TODO What is GFSR
    """

    def __init__(self, series='GFSR', search_terms=None, countries=None, period='A',
                 start_date="2000-01-01", end_date="2022-10-20"):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date)
