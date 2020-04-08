import csv

import requests


import config

class DataLoader:

    def __init__(self, live=False):
        self.live = live
        self.confirmed = None
        self.recovered = None
        self.deaths = None
        self.us_cases = None
        self.us_deaths = None
        self.confirmed_raw = None
        self.recovered_raw = None
        self.deaths_raw = None
        self.us_cases_raw = None
        self.us_deaths_raw = None
        self.update_string = ''
        self.update_date_stamp = ''
        self.load_jh_data()

    def load_jh_data(self):
        if self.live:
            self.confirmed = requests.get(config.JH_CONFIRMED_CASES)
            self.recovered = requests.get(config.JH_RECOVERED_CASES)
            self.deaths = requests.get(config.JH_DEATHS)
            self.us_cases = requests.get(config.JH_US_CASES)
            self.us_deaths = requests.get(config.JH_US_DEATHS)
        else:
            self.confirmed = requests.get(config.CONFIRMED_CASES)
            self.recovered = requests.get(config.RECOVERED_CASES)
            self.deaths = requests.get(config.DEATHS)
            self.us_cases = requests.get(config.US_CASES)
            self.us_deaths = requests.get(config.US_DEATHS)

            # self.confirmed = s3.Object('covidbio-covid-data', "confirmed.csv")
            # self.recovered = s3.Object('covidbio-covid-data', "recovered.csv")
            # self.deaths = s3.Object('covidbio-covid-data', "deaths.csv")
            #
            # self.confirmed_raw = self.confirmed.get()['Body'].read().decode('utf-8')
            # self.recovered_raw = self.recovered.get()['Body'].read().decode('utf-8')
            # self.deaths_raw = self.deaths.get()['Body'].read().decode('utf-8')

        self.confirmed_raw = self.convert_to_raw_data(self.confirmed)
        self.recovered_raw = self.convert_to_raw_data(self.recovered)
        self.deaths_raw = self.convert_to_raw_data(self.deaths)

        self.us_cases_raw = self.convert_to_raw_data(self.us_cases)
        self.us_deaths_raw = self.convert_to_raw_data(self.us_deaths)

        self.update_string = requests.get(config.UPDATE_STRING).content.decode('utf-8')
        self.update_date_stamp = requests.get(config.UPDATE_DATE_STAMP).content.decode('utf-8')

    def convert_to_raw_data(self, response):
        decoded_content = response.content.decode('utf-8')
        data = csv.reader(decoded_content.split('\n'))
        # for row in data:
        #     print(row)
        return data