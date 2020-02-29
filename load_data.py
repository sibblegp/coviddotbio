import csv

import requests


import config

class DataLoader:

    def __init__(self):
        self.confirmed_raw = None
        self.recovered_raw = None
        self.deaths_raw = None
        self.load_jh_data()

    def load_jh_data(self):
        confirmed = requests.get(config.JH_CONFIRMED_CASES)
        recovered = requests.get(config.JH_RECOVERED_CASES)
        deaths = requests.get(config.JH_DEATHS)

        self.confirmed_raw = self.convert_to_raw_data(confirmed)
        self.recovered_raw = self.convert_to_raw_data(recovered)
        self.deaths_raw = self.convert_to_raw_data(deaths)

    def convert_to_raw_data(self, response):
        decoded_content = response.content.decode('utf-8')
        data = csv.reader(decoded_content.split('\n'))
        # for row in data:
        #     print(row)
        return data