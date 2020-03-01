class Analytics:

    def __init__(self, confirmed_raw, recovered_raw, deaths_raw):
        self.general_data_format = {
                "totals": {
                    "confirmed": 0,
                    "infected": 0,
                    "recovered": 0,
                "dailies": {
                    "confirmed": [],
                    "infected": [],
                    "recovered": [],
                    }
                }
            }
        self.confirmed_raw = confirmed_raw
        self.recovered_raw = recovered_raw
        self.deaths_raw = deaths_raw
        self.primary_data = None
        self.confirmed_time_series = self.munge_csv_data(self.confirmed_raw)
        self.recovered_time_series = self.munge_csv_data(self.recovered_raw)
        self.deaths_time_series = self.munge_csv_data(self.deaths_raw)
        self.countries = self.get_countries_regions()
        # print(self.countries)
        self.gather_country_region_data(self.confirmed_time_series, "confirmed")
        self.gather_country_region_data(self.recovered_time_series, "recovered")
        self.gather_country_region_data(self.deaths_time_series, "deaths")
        self.totals = {}
        self.set_country_totals()
        print(self.countries['Mainland China'])
        print(self.totals)

    def set_country_totals(self):
        total_infected = 0
        total_confirmed = 0
        total_recovered = 0
        total_deaths = 0

        total_daily_infected = [0 for x in range(0, self.date_count)]
        total_daily_confirmed = [0 for x in range(0, self.date_count)]
        total_daily_recovered = [0 for x in range(0, self.date_count)]
        total_daily_deaths = [0 for x in range(0, self.date_count)]
        for country in self.countries.keys():
            infected = 0
            confirmed = 0
            recovered = 0
            deaths = 0

            for region in self.countries[country]["regions"].keys():
                # Add to overall totals
                infected += self.countries[country]["regions"][region]["totals"]["infected"]
                confirmed += self.countries[country]["regions"][region]["totals"]["confirmed"]
                recovered += self.countries[country]["regions"][region]["totals"]["recovered"]
                deaths += self.countries[country]["regions"][region]["totals"]["deaths"]

                # Add to country dailies
                daily_confirmed = self.countries[country]["regions"][region]["dailies"]["confirmed"]
                daily_infected = self.countries[country]["regions"][region]["dailies"]["infected"]
                daily_recovered = self.countries[country]["regions"][region]["dailies"]["recovered"]
                daily_deaths = self.countries[country]["regions"][region]["dailies"]["deaths"]

                for i in range(0, len(daily_confirmed)):
                    # Set Country dailies
                    self.countries[country]["dailies"]["confirmed"][i] += daily_confirmed[i]
                    self.countries[country]["dailies"]["infected"][i] += daily_infected[i]
                    self.countries[country]["dailies"]["recovered"][i] += daily_recovered[i]
                    self.countries[country]["dailies"]["deaths"][i] += daily_deaths[i]

                    # Add to overall dailies
                    total_daily_confirmed[i] += daily_confirmed[i]
                    total_daily_infected[i] += daily_infected[i]
                    total_daily_recovered[i] += daily_recovered[i]
                    total_daily_deaths[i] += daily_deaths[i]

                if region == country:
                    del self.countries[country]["regions"]


            # Set country totals
            self.countries[country]["totals"]["infected"] = infected
            self.countries[country]["totals"]["confirmed"] = confirmed
            self.countries[country]["totals"]["recovered"] = recovered
            self.countries[country]["totals"]["deaths"] = deaths

            total_confirmed += confirmed
            total_recovered += recovered
            total_infected += infected
            total_deaths += deaths

        self.totals["totals"] = {
            "confirmed": total_confirmed,
            "infected": total_infected,
            "recovered": total_recovered,
            "deaths": total_deaths,
        }

        self.totals["dailies"] = {
            "confirmed": total_daily_confirmed,
            "infected": total_daily_infected,
            "recovered": total_daily_recovered,
            "deaths": total_daily_deaths,
        }

    def munge_csv_data(self, dataset):
        rows = []
        for row in dataset:
            rows.append(row)
        rows = rows[1:]
        return rows

    def gather_country_region_data(self, dataset, name):
        for row in dataset:
            region = row[0]
            country = row[1]
            if region == '':
                region = country
            self.countries[country]["regions"][region]["totals"][name] = self.get_row_total(row)
            self.countries[country]["regions"][region]["dailies"][name] = [int(x) for x in row[4:]]

    def get_row_total(self, row):
        return int(row[-1])

    def get_column_total(self, data, column_number):
        return sum([row[column_number] for row in data])

    def get_countries_regions(self):
        countries = {}
        for row in self.confirmed_time_series:
            country = row[1]
            region = row[0]
            if region == '':
                region = country
            if country not in countries:
                countries[country] = {
                    "totals": {
                        "confirmed": 0,
                        "infected": 0,
                        "recovered": 0,
                        "deaths": 0,
                    },
                    "dailies": {
                        "confirmed": [0 for x in range(0, self.date_count)],
                        "infected": [0 for x in range(0, self.date_count)],
                        "recovered": [0 for x in range(0, self.date_count)],
                        "deaths": [0 for x in range(0, self.date_count)],
                        },
                    "regions": {}
                    }

            print(region)
            countries[country]["regions"][region] = {
                "totals": {
                    "confirmed": 0,
                    "infected": 0,
                    "recovered": 0,
                    "deaths": 0,
                },
                "dailies": {
                    "confirmed": [0 for x in range(0, self.date_count)],
                    "infected": [0 for x in range(0, self.date_count)],
                    "recovered": [0 for x in range(0, self.date_count)],
                    "deaths": [0 for x in range(0, self.date_count)]
                    }
                }


        return countries


    @property
    def date_count(self):
        return len(self.confirmed_time_series[0][4:])