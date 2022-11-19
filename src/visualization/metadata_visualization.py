import requests
from pyquery import PyQuery as pq
import pandas as pd
import time as tm
import json
import numpy as np

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'


class series:
    def __init__(self):
        self.series_list = []
        self.series_dict = {}
        self.size = 0
        self._load_data()

    def _load_data(self):
        df_url = f"{url}Dataflow"
        tmp_json = requests.get(f'{df_url}').json()['Structure']['Dataflows']['Dataflow']
        for tj in tmp_json:
            code = tj['KeyFamilyRef']['KeyFamilyID']
            name = tj['Name']['#text']

            if not any(char.isdigit() for char in name):
                self.series_dict[code] = name
                self.series_list.append(code)
                self.size = self.size + 1

        self.series_list.sort()
        self.series_dict = dict(sorted(self.series_dict.items()))

    def search(self, search_term=None):
        print(f"Series matching '{search_term}'")
        print("----------------------------------------------------")
        for key in self.series_dict:
            if search_term in self.series_dict[key]:
                print(key, ": ", self.series_dict[key])

    def __repr__(self):
        return '[' + ','.join(repr(self.series_list[i]) for i in range(self.size)) + ']'




class main:
    search_term = 'Financial Statistics'
    series = series()
    series.search(search_term)
    print(series.__sizeof__())
    print(series.size)


