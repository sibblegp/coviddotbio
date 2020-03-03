import csv

import requests


import config

class DataLoader:

    def __init__(self, live=False):
        self.live = live
        self.confirmed = None
        self.recovered = None
        self.deaths = None
        self.confirmed_raw = None
        self.recovered_raw = None
        self.deaths_raw = None
        self.load_jh_data()

    def load_jh_data(self):
        if self.live:
            self.confirmed = requests.get(config.JH_CONFIRMED_CASES)
            self.recovered = requests.get(config.JH_RECOVERED_CASES)
            self.deaths = requests.get(config.JH_DEATHS)
        else:
            self.confirmed = requests.get(config.CONFIRMED_CASES)
            self.recovered = requests.get(config.RECOVERED_CASES)
            self.deaths = requests.get(config.DEATHS)


        self.confirmed_raw = self.convert_to_raw_data(self.confirmed)
        self.recovered_raw = self.convert_to_raw_data(self.recovered)
        self.deaths_raw = self.convert_to_raw_data(self.deaths)

    def convert_to_raw_data(self, response):
        decoded_content = response.content.decode('utf-8')
        data = csv.reader(decoded_content.split('\n'))
        # for row in data:
        #     print(row)
        return data