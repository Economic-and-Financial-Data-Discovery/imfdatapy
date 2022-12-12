"""
Authors: Sou-Cheng T. Choi and Irina Klein, Illinois Institute of Technology
Updated Date: Dec 7, 2022
Creation Date: Jun 15, 2022

"""
import itertools
import logging
import logging.config
import os
import time as tm
from abc import ABC, abstractmethod
from datetime import datetime
from os import mkdir
from os import path
import itertools

import pandas as pd
import requests

MAX_FILENAME_LEN = 260

# Create logger
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__) # TODO is it logger or logging later
time_stamp = str(datetime.now())[:16].replace(" ", "-").replace(":", "-")
# Doesn't create new directory in colab
logdir = '../../log'
if not path.exists(logdir):
    mkdir(logdir)
logging.basicConfig(filename=f'{logdir}/imf_{time_stamp}.log', encoding='utf-8', level=logging.info)


# abstract class
class Series(ABC):

    def __init__(self, series='IFS', search_terms=None, countries=None, period='Q', start_date=None, end_date=None,
                 outdir=None):
        """
        This function initializes the IMF class, which is used to download data from the IMF's Data API.

        Args:
          series: the name of the series to download. Defaults to 'IFS'.
          search_terms: list of strings to find in indicator names in the series.
          countries: list of strings containing ISO-2 code of country names.
          period: frequency of time series. Defaults to 'Q'.
          start_date: The start date of the time series, e.g, 2000-01-01. Defaults to None to get the earliest date of data.
          end_date: The end date of the time series, e.g, 2022-10-20. Defaults to None to get the latest date of data.
          outdir: the directory where the data will be saved
        """
        input_str = ""
        if series is not None:
            input_str += f"{series = }"
        if search_terms is not None:
            input_str += f", {search_terms = }"
        if countries is not None:
            input_str += f", {countries = }"
        if start_date is not None:
            input_str += f", {start_date = }"
        if end_date is not None:
            input_str += f", {end_date = }"
        if outdir is not None:
            input_str += f", {outdir = }"
        logger.info(f"Inputs: {input_str}")

        self.series = series
        self.search_terms = search_terms
        self.countries = countries
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.start_time = start_date[:4] if isinstance(start_date, str) else start_date
        self.end_time = end_date[:4] if isinstance(end_date, str) else end_date
        self.url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
        self.meta_df = pd.DataFrame()
        self.series_df = pd.DataFrame()
        self.data_df = pd.DataFrame()
        self.dim_dict = {}
        self.des_list = []
        self.id_list = []

        # Control for rate limits, `https://datahelp.imf.org/knowledgebase/articles/630877-data-services`
        self._max_requests = 3
        self._sleep_sec = 2
        self._max_indicators = 5

        # Doesn't create new directory in colab
        self.outdir = outdir if outdir is not None else f"..{os.sep}out{os.sep}"
        if not path.exists(self.outdir):
            mkdir(self.outdir)

    def get_series_names(self):
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
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series, search_terms, countries, period, start_date, end_date, outdir)

    def output_series(self, series=None):
        """
        This function outputs all or some IMF series dataframe to a csv file, and logs its file path.


        Args:
          series: Series code as a string. If `series` is `None`, then the function outputs all series to a csv file. If `series` is not `None`, then the function outputs only the series that contain the string `series` to a csv file.
        """

        # output to csv file
        if series is None:
            outfile_path = f"{self.outdir}series_imf.csv"
        else:
            outfile_path = f"{self.outdir}series_{series.lower()}.csv"
        if (self.series_df.shape[0] > 0) and (self.series_df.shape[1] > 0):
            self.series_df.to_csv(outfile_path, index=False)
            if series is None:
                logger.info(f"Output all IMF series in a {self.series_df.shape} table to {outfile_path}")
            else:
                logger.info(f"Output series containing '{series}' in a {self.series_df.shape} table to {outfile_path}")
        else:
            logger.warning(f"No series data to be output")

    def output_dim(self, dim_name=None):
        """
        This function outputs all or some dimension tables to a .csv file in 'out'

        Args:
          dim_name: Dimension name as a string
        """
        # output to csv file
        if dim_name is None:
            for key in self.dim_dict.keys():
                outfile_path = f"{self.outdir}dim_{key.lower()}.csv"
                if (self.dim_dict[key].shape[0] > 0) and (self.dim_dict[key].shape[1] > 0):
                    self.dim_dict[key].to_csv(outfile_path, index=False)
                    logger.info(f"Output dimension {key} in a {self.dim_dict[key].shape} table to {outfile_path}")
                else:
                    logger.warning(f"No dimension {key} data to be output.")
        else:
            key = dim_name
            outfile_path = f"{self.outdir}dim_{key.lower()}.csv"
            if (self.dim_dict[key].shape[0] > 0) and (self.dim_dict[key].shape[1] > 0):
                self.dim_dict[key].to_csv(outfile_path, index=False)
                logger.info(f"Output dimension {key} in a {self.dim_dict[key].shape} table to {outfile_path}")
            else:
                logger.warning(f"No dimension {key} data to be output.")

    def output_meta(self, indicator=None):
        """
        Method to output all or some indicators in a tables to a .csv file in 'out'

        Args:
          indicator: Indicator code as a string
        """

        # output to csv file
        if indicator is None:
            outfile_path = f"{self.outdir}meta_{self.series.lower()}.csv"
        else:
            csv_filename, st_str = self.gen_data_filename(is_meta=True)
            outfile_path = f"{self.outdir}{csv_filename}"
        if (self.meta_df.shape[0] > 0) and (self.meta_df.shape[1] > 0):
            self.meta_df.to_csv(outfile_path, index=False)
            if indicator is None:
                logger.info(f"Output meta data of {self.series} in a {self.meta_df.shape} table to {outfile_path}")
            else:
                logger.info(f"Output meta data of {self.series} with search search_terms {self.search_terms} in a {self.meta_df.shape} table to {outfile_path}")
        else:
            logger.warning(f"No meta data to be output.")

    def output_data(self, is_gen_filename=False):
        """
        This function outputs the data to a csv file.

        Args:
          is_gen_filename: generate the csv file name from user inputs if `True`, defaults to `False`
        """
        # output to csv file
        if not is_gen_filename:
            outfile_path = f"{self.outdir}data_{self.series.lower()}.csv"
        else:
            csvfilename, st_str = self.gen_data_filename()
            outfile_path = f"{self.outdir}{csvfilename}"

        if (self.data_df.shape[0] > 0) and (self.data_df.shape[1] > 0):
            self.data_df.to_csv(outfile_path, index=False)
            if not is_gen_filename:
                logger.info(f"Output data of {self.series} in a {self.data_df.shape} table to {outfile_path}")
            else:
                logger.info(f"Output data of {self.series} containing '{st_str}' in a {self.data_df.shape} table to {outfile_path}")
        else:
            logger.warning(f"No data to be output.")

    def gen_data_filename(self, is_meta=False):
        """
        It takes the search terms, countries, period, start time, and end time, and creates a filename for
        the data up to 250 characters

        Args:
          is_meta: whether to generate a filename for the meta data or the actual data, defaults to False
        (optional). Defaults to False

        Returns:
          The filename and the search terms
        """
        if len(self.search_terms) > 3:
            st_str = "_".join(self.search_terms[:3]) + f"_{len(self.search_terms) - 3}"
        else:
            st_str = "_".join(self.search_terms)
        if len(self.countries) > 5:
            ctry_str = "_".join(self.countries[:5]) + f"_{len(self.countries) - 5}"
        else:
            ctry_str = "_".join(self.countries)

        time = ''
        if self.start_time is not None and self.end_time is not None:
            time = f'_{self.start_time}_{self.end_time}'
        if self.start_time is None and self.end_time is not None:
            time = f'_{self.end_time}'
        if self.start_time is not None and self.end_time is None:
            time = f'_{self.start_time}_'

        if not is_meta:
            csv_filename = f"data_{st_str}_{ctry_str}_{self.period}{time}"[:MAX_FILENAME_LEN]
        else:
            csv_filename = f"meta_{st_str}_{ctry_str}_{self.period}{time}"[:MAX_FILENAME_LEN]
        csv_filename = f"{csv_filename}.csv"
        return csv_filename, st_str

    # overriding abstract methods
    def get_series_names(self):
        """
        It takes a list of series names, and returns a dataframe with the series names and their
        corresponding IDs

        Returns:
          A dataframe with the series names and their corresponding IDs.
        """

        # searches through series:
        key = 'Dataflow'  # Method with series information
        search_terms = self.series  # search terms to find in series names
        # define the URL we want to use, make a request to the IMF data server
        json = self.repeat_request(url=f'{self.url}{key}')
        # check if the request was successful
        if json is not None:
            # found series names
            series_list = json['Structure']['Dataflows']['Dataflow']
            # normalize the JSON data
            self.series_df = pd.json_normalize(series_list)
            self.series_df = self.series_df.sort_values("KeyFamilyRef.KeyFamilyID")
            self.series_df = self.clean_column_names(self.series_df)
            # output the data to a CSV file
            self.output_series()
            is_output = True
        else:
            infile = f"{self.outdir}series_{self.series.lower()}.csv"
            self.series_df = pd.read_csv(infile)
            logger.info(f"Read series names from historical data {infile}")
            is_output = False

        # Filter the dataframe to only include the series names we want
        self.series_df["search_found"] = False
        string_columns = self.series_df.select_dtypes(include=object).columns
        for col, search_term in itertools.product(string_columns, [search_terms]):
            logger.debug(f"{col = }, {search_term = }")
            self.series_df["search_found"] = self.series_df["search_found"] | self.series_df[
                col].str.lower().str.contains(
                search_term.lower())
            logger.debug(self.series_df["search_found"].describe())
        self.series_df = self.series_df[self.series_df["search_found"]]
        self.series_df = self.series_df.drop(['search_found'], axis=1)
        if self.series_df.shape[0] == 0:
            logger.error(f"Input search terms '{search_terms}' do not exist. See column 'KEYFAMILYREF.KEYFAMILYID' in '{self.outdir}series_imf.csv' for valid values.")
            return None
        if is_output:
            # output the data to a CSV file
            self.output_series(series=self.series)

        logger.debug(self.series_df.head())
        return self.series_df

    def get_dimensions(self):
        """
        It downloads the dimensions of the series, and then downloads the details of each dimension
        """

        # finds the dimensions in the series. We need the indicators.
        key = f'DataStructure/{self.series}'  # DataStructure Method / series
        json = self.repeat_request(url=f'{self.url}{key}')
        if json is not None:
            self.dimension_list = json['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
            self.dim_df = pd.json_normalize(self.dimension_list)

            # finds the indicators by the search words:
            for n, dimension in enumerate(self.dimension_list):
                self.des_list.extend([n + 1])
                self.id_list.extend([dimension['@codelist']])
                logger.debug(f"Dimension {n + 1}: {dimension['@codelist']}")
            self.dim_meta_df = pd.DataFrame(list(zip(self.des_list, self.id_list)), columns=['Dimension', 'ID'])
            self.dim_meta_df = self.dim_meta_df.sort_values("Dimension")

            for n in range(0, len(self.dimension_list)):
                is_output = True
                try:
                    dim_name = self.dimension_list[n]['@codelist']
                    key = f"CodeList/{dim_name}"
                    if dim_name[:7] in ["CL_FREQ"]:
                        def _get_metadata(series='IFS'):
                            """
                            The function `_get_metadata` takes a single argument, `series`, which is a string that defaults to
                            `'IFS'`. The function then uses the `repeat_request` function to make a request to the
                            `GenericMetadata` endpoint of the API, and if the request is successful, it returns the
                            `AttributeValueSet` of the `MetadataSet` of the `GenericMetadata` of the response

                            Args:
                              series: The data series you want to download. Defaults to `IFS`

                            Returns:
                              A list of dictionaries containing metadata.
                            """
                            key = f'GenericMetadata/{series}'
                            json = self.repeat_request(url=f'{self.url}{key}')
                            if json is not None:
                                metadata = json['GenericMetadata']['MetadataSet']['AttributeValueSet']
                            else:
                                metadata = None
                            return metadata

                        def _extract_metadata(metadata, indicator='FREQ'):
                            """
                            Given an economic indicator name, the function takes in a list of dictionaries, and returns a dataframe with two columns, one for
                            the valid values and one for the value description of the indicator.

                            Args:
                              metadata: the metadata dictinoary from the API call
                              indicator: The indicator we want to get data for. Defaults to 'FREQ'.

                            Returns:
                              A dataframe with the value and description of the frequency of the data.
                            """
                            if metadata is None:
                                return pd.DataFrame()

                            des_list, value_list = [], []
                            for i in range(len(metadata)):
                                ind = metadata[i]['ReportedAttribute'][1]['@conceptID']
                                if ind == indicator:
                                    output = metadata[i]['ReportedAttribute'][1]['ReportedAttribute']
                                    logger.debug(output[0]['Value']['#text'], ": ", output[2]['Value']['#text'])
                                    des_list.extend([output[0]['Value']['#text']])
                                    value_list.extend([output[2]['Value']['#text']])

                            df = pd.DataFrame.from_dict({"Value": value_list, "Description": des_list})
                            return df

                        _metadata = _get_metadata(series=self.series)
                        if dim_name[-4:].lower() != self.series.lower():
                            dim_name = "_".join([dim_name, self.series])
                        if _metadata is not None:
                            code_df = _extract_metadata(metadata=_metadata, indicator='FREQ')
                            code_df = self.clean_column_names(code_df)
                            self.dim_dict[dim_name] = code_df
                            logger.debug(f"Dimension {dim_name} details: \n{code_df}")
                            self.output_dim(dim_name)
                        else:
                            logger.warning(f"Failed to download dimension, CL_FREQ.")
                            self.read_dim_df(dim_name=dim_name)
                    else:
                        json = self.repeat_request(url=f'{self.url}{key}')
                        if json is not None:
                            code_list = json['Structure']['CodeLists']['CodeList']['Code']
                            code_df = pd.json_normalize(code_list)
                            code_df = self.clean_column_names(code_df)
                            self.dim_dict[dim_name] = code_df
                            logger.debug(f"Dimension {dim_name} details: \n{code_df}")
                            self.output_dim(dim_name)
                        else:
                            logger.warning(f"Failed to download dimension {dim_name}.")
                            self.read_dim_df(dim_name=dim_name)

                except:
                    pass
        else:
            logger.warning(f"Failed to download dimensions.")

    def download_meta(self):
        """
        The function downloads the meta data of the time series from the IMF API

        Returns:
          The meta data of the time series.
        """

        if len(self.dimension_list) == 0:
            self.read_meta_df()
        else:
            # finds the indicators by the search words:
            for n, dimension in enumerate(self.dimension_list):
                self.des_list.extend([n + 1])
                self.id_list.extend([dimension['@codelist']])
                # logger.debug(f"Dimension {n + 1}: {dimension['@codelist']}")
            dim_meta_df = pd.DataFrame(list(zip(self.des_list, self.id_list)), columns=['Dimension', 'ID'])
            dim_meta_df = dim_meta_df.sort_values("Dimension")
            dim_meta_df = self.clean_column_names(dim_meta_df)
            logger.debug(dim_meta_df.head())

            # download  meta data
            key = f"CodeList/{self.dimension_list[2]['@codelist']}"
            json = self.repeat_request(url=f'{self.url}{key}')
            if json is not None:
                code_list = json['Structure']['CodeLists']['CodeList']['Code']
                self.meta_df = pd.json_normalize(code_list)
                self.meta_df = self.clean_column_names(self.meta_df)
                self.output_meta()
            else:
                self.read_meta_df()

        # finds the indicators by the search words
        key = f"CodeList/{self.dimension_list[2]['@codelist']}"
        json = self.repeat_request(url=f'{self.url}{key}')
        if json is not None:
            code_list = json['Structure']['CodeLists']['CodeList']['Code']
            self.meta_df = pd.json_normalize(code_list)

            self.meta_df["search_found"] = False
            string_columns = self.meta_df.select_dtypes(include=object).columns
            for col, search_term in itertools.product(string_columns, self.search_terms):
                logger.debug(f"{col = }, {search_term = }")
                self.meta_df["search_found"] = self.meta_df["search_found"] | \
                                               self.meta_df[col].str.lower().str.contains(search_term.lower())
                logger.debug(self.meta_df["search_found"].describe())
                logger.debug(self.meta_df[self.meta_df["search_found"]])
            self.meta_df = self.meta_df[self.meta_df["search_found"]]
            self.meta_df = self.meta_df.drop(['search_found'], axis=1)

            if self.meta_df.shape[0] == 0:
                logger.error(f"User input search terms {self.search_terms} not found in {self.series}. Please see columns 'VALUE' or 'DESCRIPTION.TEXT' in {self.outdir}meta_{self.series}.csv for valid values.")
                return None

            if "ID" not in self.meta_df.columns:
                self.meta_df.columns = ["ID", *list(self.meta_df.columns)[1:]]
            if "Description" not in self.meta_df.columns:
                self.meta_df.columns = [*list(self.meta_df.columns)[:-1], "Description"]
            logger.debug(f"{self.meta_df.shape = }")
            self.meta_df = self.clean_column_names(self.meta_df)

            # deduplicate
            self.meta_df = self.meta_df.drop_duplicates(keep='last')

            self.output_meta(indicator="")
        else:
            logger.warning(f"Failed to download meta data.")
            self.read_meta_df()

        return self.meta_df

    def read_meta_df(self):
        """
        The function reads a csv file into a Pandas dataframe, renames the columns, and then cleans the column names.

        """
        infile = f"{self.outdir}meta_{self.series.lower()}.csv"
        self.meta_df = pd.read_csv(infile)
        self.meta_df = self.meta_df.rename(
            columns={
                '@value': 'ID',
                'Description.#text': 'Description'
            }
        )
        self.meta_df = self.clean_column_names(self.meta_df)
        logger.info(f"Read meta information from historical data {infile}")


    def read_dim_df(self, dim_name="CL_FREQ"):
        """
        The function reads a csv file with dimension data into a Pandas dataframe.

        Args:
            dim_name: name of dimension
        """
        infile = f"{self.outdir}dim_{dim_name.lower()}.csv"
        if path.exists(infile):
            self.dim_dict[dim_name] = pd.read_csv(infile)
            logger.info(f"Read dimension information from historical data {infile}")
        else:
            self.dim_dict[dim_name] = None


    # overriding abstract method
    def download_data(self):
        """
        It downloads data and its meta data from the IMF web server, and saves it to a csv file.

        Returns:
          The data is being returned as a pandas dataframe.
        """
        if self.get_series_names() is None:
            return None

        self.get_dimensions()
        self.validate_inputs()

        self.meta_df = self.download_meta()
        if self.meta_df is None:
            return None


        base = f'{self.url}CompactData/{self.series}/'
        time = ''
        if self.start_time is not None and self.end_time is not None:
            time = f'.?startPeriod={self.start_time}&endPeriod={self.end_time}'
        if self.start_time is None and self.end_time is not None:
            time = f'.?endPeriod={self.end_time}'
        if self.start_time is not None and self.end_time is None:
            time = f'.?startPeriod={self.start_time}'

        self.data_df = pd.DataFrame()
        # sometimes a big list of country codes results in an error, try splitting it into 2 lists and running this and next cell twice.
        dcn_sa = list(self.meta_df["ID"].values)
        temp = pd.DataFrame()

        if self.countries[0] == '':
            dcn_sa_list = [dcn_sa[x:x + self._max_indicators] for x in range(0, len(dcn_sa), self._max_indicators)]
        else:
            dcn_sa_list = [dcn_sa[x:x + 1] for x in range(0, len(dcn_sa), 1)]

        for cont, indicators in itertools.product(self.countries,  dcn_sa_list):
            logger.debug("Current country", cont)
            url = f"{base}{self.period}.{cont}.{'+'.join(indicators)}{time}"
            # url = f"{base}{period}..{'+'.join(indicators)}.{time}"
            logger.debug(f"{url = }")
            json = self.repeat_request(url)
            if json is not None:
                try:
                    response = json
                    series = response['CompactData']['DataSet']['Series']
                    temp_df = pd.DataFrame()
                    if isinstance(series, dict):
                        if isinstance(series.get("Obs"), list):
                            temp_df = pd.concat([temp_df, pd.json_normalize(series.get("Obs"))])
                        for k in series.keys():
                            if k != "Obs":
                                temp_df[k] = series.get(k)

                        if temp_df.shape[0] > 0:
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

                            for k in series[n].keys():
                                if k != "Obs":
                                    temp_df[k] = series[n].get(k)

                            if temp_df.shape[0] > 0:
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
                    logger.warning(f"Request for IMF data failed for area code, {cont}: {url = }.")
                    pass

        is_output = True
        if temp.shape[0] == 0:
            csv_filename, _ = self.gen_data_filename()
            outfile_path = f"{self.outdir}{csv_filename}"
            if path.exists(outfile_path):
                temp = pd.read_csv(outfile_path)
                logger.warning(f"Read data from historical file {outfile_path}")
                if "Description" in temp.columns:
                    temp = temp.drop(['Description'], axis=1)
                is_output = False
            else:
                logger.warning(f"No data has been downloaded.")
                return pd.DataFrame()

        self.data_df = pd.concat([temp, self.data_df], axis=0)
        self.data_df = pd.merge(self.data_df, self.meta_df, on="ID", how="left")

        # deduplicate
        self.data_df = self.data_df.drop_duplicates(keep='last')

        # sorting
        self.data_df.sort_values(by=["ID", "Country", 'Period'], axis=0, inplace=True)
        logger.debug(f"data_df.shape = {self.data_df.shape}")

        # remove special characters in column names
        self.data_df = self.clean_column_names(self.data_df)

        if is_output:
            self.output_data(is_gen_filename=True)

        return self.data_df

    def validate_inputs(self):
        """
        The function checks if the user inputs are valid. It will change an invalid input to a valid value with a warning.
        """

        # check period and correct wrong value
        freq_key = f"CL_FREQ_{self.series.upper()}"
        if (freq_key in self.dim_dict.keys()) and (self.dim_dict[freq_key] is not None):
            valid_periods = self.dim_dict[freq_key]["VALUE"].values
            valid_periods_str = ", ".join(valid_periods)
            if not (self.period in valid_periods):
                logger.warning(f"Input period '{self.period}' is not valid (See CL_AREA_{self.series} output table). Changing it to '{valid_periods[0]}'.")
                self.period = valid_periods[0]

        # validate start date and end date
        def _validate_date(date, date_des):
            """
            It takes in a date and a description of the date, and if the date is not in the correct format, it
            logs a warning and returns None.

            Args:
              date: The date of the data you want to get.
              date_des: description of the date, used for logger.

            Returns:
              A valid date
            """
            try:
                if date is not None:
                    datetime.strptime(date, "%Y")
            except ValueError:
                logger.warning(f"Incorrect data format in input {date_des}, should be 'YYYY'. Setting it to 'None'.")
                date = None
            return date

        self.start_time = _validate_date(self.start_time, "start_date")
        self.end_time = _validate_date(self.end_time, "end_date")

        # check country and correct wrong value
        area_key = f"CL_AREA_{self.series.upper()}"
        if (area_key in self.dim_dict.keys()) and (self.dim_dict[area_key] is not None):
            valid_countries = self.dim_dict[area_key]["VALUE"].values
            if self.countries is None:
                self.countries = ['']
            rm_countries = []
            for c in self.countries:
                if not (c in valid_countries):
                    logger.warning(f"Input country '{c}' is not valid (see CL_AREA_{self.series}'s output table). Dropping it from input.")
                    rm_countries.extend([c])
            for c in rm_countries:
                self.countries.remove(c)
            if len(self.countries) == 0:
                logger.warning(f"Input countries contains no valid entries. Setting it to [{valid_countries[0]}]")
                self.countries = [valid_countries[0]]

        # validate serarch terms
        if self.search_terms is None:
            self.search_terms = self.meta_df.iloc[:, -1].values

    def clean_column_names(self, df):
        """
        It replaces special characters in all column names and makes them upper case

        Args:
          df: The Pandas dataframe to be cleaned

        Returns:
          The Pandas dataframe with the cleaned column names.
        """

        df.columns = df.columns.str.replace('[@]',   '',  regex=True).  \
                                str.replace('[#,:]', '_', regex=True).  \
                                str.replace("._",    '.', regex=False). \
                                str.upper()
        return df

    def repeat_request(self, url):
        """
        It will try to get a response from the IMF data server for a given url, and if it doesn't get a
        response, it will wait a few seconds and try again

        Args:
          url: the url to request

        Returns:
          The json object is being returned. It will returns `None` if it does not get a valid response after making a few requests to the IMF data server.
        """

        json = None
        for _ in range(self._max_requests):
            tm.sleep(self._sleep_sec)
            rq = requests.get(url)
            if rq.status_code == 200:
                try:
                    json = rq.json()
                except:
                    # print a warning message to the console if it does not gets a valid response from the IMF data server
                    if isinstance(json, dict) and (len(json) >= 1):  # actrally valid response
                        return json

        if not (isinstance(json, dict) and (len(json) >= 1)):
            # check that the JSON object is a dictionary, and that it has more than one key, otherwise gives a warning
            logger.warning(f"No response received from IMF data server for {url = } after {self._max_requests} trials.")
            json = None

        return json

    # overriding abstract method
    def get_meta(self):
        """
        This function returns the meta data of the IMF economic indicator(s).

        Returns:
          The meta data of the time series data
        """
        return self.meta_df

    # overriding abstract method
    def get_data(self):
        """
        This function returns the time series data.

        Returns:
          The dataframe of the time series data.
        """

        return self.data_df

    def describe_data(self):
        """
        The function returns a summary of data.

        Returns:
          A Pandas dataframe that contains the summary statistics of the data.
        """

        self.data_summary_df = self.data_df.groupby(["ID", "COUNTRY"]).describe(include="all", datetime_is_numeric=True).T
        return self.data_summary_df

    def describe_meta(self):
        """
        This function takes the meta data dataframe and returns a summary of the meta data.

        Returns:
            Summary of meta data
        """
        self.meta_summary_df = self.meta_df.describe(include="all", datetime_is_numeric=True)
        return self.meta_summary_df


class AFRREO(IMF):
    """
    Sub-Saharan Africa Regional Economic Outlook (AFRREO). A child class of IMF.
    """

    def __init__(self, series='AFRREO', search_terms=None, countries=None, period='Q',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class IFS(IMF):
    """
    International Financial Statistics (IFS). A child class of IMF.
    """

    def __init__(self, series='IFS', search_terms=None, countries=None, period='Q',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class DOT(IMF):
    """ Direction of Trade Statistics (DOT). A child class of IMF.

    """

    def __init__(self, series='DOT', search_terms=None, countries=None, period='Q',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class BOP(IMF):
    """
    Balance of Payments (BOP). A child class of IMF.
    """

    def __init__(self, series='BOP', search_terms=None, countries=None, period='Q',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class FSI(IMF):
    """
    Financial Soundness Indicators (FSIs). A child class of IMF.

    """

    def __init__(self, series='FSI', search_terms=None, countries=None, period='M',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class GFSR(IMF):
    """
    Government Finance Statistics (GFS), Revenue. A child class of IMF.
    """

    def __init__(self, series='GFSR', search_terms=None, countries=None, period='A',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


class COFOG(IMF):
    """
    Government Finance Statistics (GFS), Expenditure by Function of Government (COFOG). A child class of IMF.
    """

    def __init__(self, series='COFOG', search_terms=None, countries=None, period='A',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


# > The `HPDD` class is a subclass of the `IMF` class. It inherits all of the methods and attributes of the `IMF` class,
# and adds a few of its own
class HPDD(IMF):
    """
     Historical Public Debt Database (HPDD). A child class of IMF.
    """

    def __init__(self, series='HPDD', search_terms=None, countries=None, period='A',
                 start_date=None, end_date=None, outdir=None):
        super().__init__(series=series, search_terms=search_terms, countries=countries, period=period,
                         start_date=start_date, end_date=end_date, outdir=outdir)


#
if __name__ == '__main__':
    ifs = IFS(search_terms=["Gross Domestic Product, Real"], countries=["US", "DE"],
              period='Q', start_date="2000", end_date="2022", outdir=f"..{os.sep}..{os.sep}out{os.sep}")
    df = ifs.download_data()
    df_summary = ifs.describe_data()