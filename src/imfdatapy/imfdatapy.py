from abc import ABC, abstractmethod
import requests
import pandas as pd
# import time as tm
import json
import numpy as np


# abstract class
class Series(ABC):

    def __init__(self, countries=["US"], start_date="2000-01-01", end_date="2022-10-20", frequency=None, indices=None):
        self.countries = countries
        self.start_date = start_date
        self.end_date = end_date
        self.indices = indices
        self.frequency = frequency
        self.metadata = None
        self.series = None
        countries_str = ", ".join(self.countries)
        print(f"{countries_str = },\n{self.start_date = }, {self.end_date = }")
        if self.indices:
            indices_str = ", ".join(self.indices)
            print(f"{indices_str = }")
        if self.frequency:
            print(frequency)

    @abstractmethod
    def download_metadata(self):
        url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/GenericMetadata/'
        key = f'{self.series}/{self.frequency}.{area}.{code}'

    @abstractmethod
    def download_data(self):
        pass

    @abstractmethod
    def summarize_data(self):
        pass


# concrete class
class IFS(Series):

    def __init__(self, countries=["US"], start_date="2000-01-01", end_date="2022-10-20", frequency=None, indices=None):
        super().__init__(countries, start_date, end_date)
        self.series = 'IFS'

    # overriding abstract method
    def download_metadata(self):
        # get metadata structure
        url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
        key = 'MetadataStructure/'
        metadata_structure = {}
        print("Loading metadata structure...")
        metadata_tmp_json = requests.get(f'{url}{key}{self.series}').json()['Structure']['Concepts']["ConceptScheme"][0]["Concept"]
        for metadata in metadata_tmp_json:
            #print(metadata["@id"])
            metadata_structure[metadata["@id"]] = []
        print("metadata_structure: ", metadata_structure)

        # get metadata
        key = 'GenericMetadata/'
        print("Loading metadata...")
        metadata = requests.get(f'{url}{key}{self.series}').json()['GenericMetadata']['MetadataSet']['AttributeValueSet']

        for dimension in metadata_structure:
            #print(dimension)
            for i in range(len(metadata)):
                dim = metadata[i]['ReportedAttribute'][1]['@conceptID']
                #print(dim)
                if dim == dimension:
                    value = metadata[i]['ReportedAttribute'][1]['ReportedAttribute']
                    metadata_structure[dimension].append(value[2]['Value']['#text'])
        print("metadata_structure: ", metadata_structure)

    def download_datastructure(self):
        url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/'
        dimension_list = []
        requests.get(f'{url}{self.series}').json()['Structure']['KeyFamilies']['KeyFamily']['Components'][
            'Dimension']
        for n, dimension in enumerate(dimension_list):
            print(f"Dimension {n + 1}: {dimension['@codelist']}")

    # overriding abstract method
    def download_data(self):
        pass

    def summarize_data(self):
        pass


if __name__ == '__main__':
    # from src.series import *

    ifs = IFS(countries=['US', 'GB'])
    ifs.download_metadata()
