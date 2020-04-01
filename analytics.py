from config import STATE_MAP
import datetime

class Analytics:

    def __init__(self, confirmed_raw, recovered_raw, deaths_raw, ignore_china=False):
        self.ignore_china = ignore_china
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
        self.dates = []
        self.confirmed_time_series = self.munge_csv_data(self.confirmed_raw)
        self.recovered_time_series = self.munge_csv_data(self.recovered_raw)
        self.deaths_time_series = self.munge_csv_data(self.deaths_raw)
        self.countries = self.get_countries_regions()

        # print(self.countries)
        self.gather_country_region_data(self.confirmed_time_series, "confirmed")
        self.gather_country_region_data(self.recovered_time_series, "recovered")
        self.gather_country_region_data(self.deaths_time_series, "deaths")
        self.gather_infected()
        self.totals = {}
        self.set_country_totals()
        # print(self.countries["China"])

    def convert_region(self, region, country):
        new_region = region
        region_parts = region.split(", ")
        if len(region_parts) > 1 and country == 'US':
            new_region = STATE_MAP[region_parts[1].strip()]
        return new_region

    def set_country_totals(self):
        total_infected = 0
        total_confirmed = 0
        total_recovered = 0
        total_deaths = 0

        total_daily_infected = [0 for x in range(0, self.date_count)]
        total_daily_confirmed = [0 for x in range(0, self.date_count)]
        total_daily_recovered = [0 for x in range(0, self.date_count)]
        total_daily_deaths = [0 for x in range(0, self.date_count)]

        total_delta_infected = [0 for x in range(0, self.date_count)]
        total_delta_confirmed = [0 for x in range(0, self.date_count)]
        total_delta_recovered = [0 for x in range(0, self.date_count)]
        total_delta_deaths = [0 for x in range(0, self.date_count)]
        for country in self.countries.keys():
            infected = 0
            confirmed = 0
            recovered = 0
            deaths = 0
            if country == "China" and self.ignore_china:
                pass
            else:
                for region in self.countries[country]["regions"].keys():
                    # Add to overall totals
                    adjusted_region = self.convert_region(region, country)
                    infected += self.countries[country]["regions"][region]["totals"]["infected"]
                    confirmed += self.countries[country]["regions"][region]["totals"]["confirmed"]
                    recovered += self.countries[country]["regions"][region]["totals"]["recovered"]
                    deaths += self.countries[country]["regions"][region]["totals"]["deaths"]

                    # Add to region dailies
                    daily_confirmed = self.countries[country]["regions"][region]["dailies"]["confirmed"]
                    daily_infected = self.countries[country]["regions"][region]["dailies"]["infected"]
                    daily_recovered = self.countries[country]["regions"][region]["dailies"]["recovered"]
                    daily_deaths = self.countries[country]["regions"][region]["dailies"]["deaths"]

                    for i in range(0, len(daily_confirmed)):
                        # Set region deltas
                        if i != 0:
                            self.countries[country]["regions"][region]["deltas"]["confirmed"][i] = \
                            self.countries[country]["regions"][region]["dailies"]["confirmed"][i] - \
                            self.countries[country]["regions"][region]["dailies"]["confirmed"][i - 1]

                            self.countries[country]["regions"][region]["deltas"]["infected"][i] = \
                                self.countries[country]["regions"][region]["dailies"]["infected"][i] - \
                                self.countries[country]["regions"][region]["dailies"]["infected"][i - 1]

                            try:
                                self.countries[country]["regions"][region]["deltas"]["recovered"][i] = \
                                    self.countries[country]["regions"][region]["dailies"]["recovered"][i] - \
                                    self.countries[country]["regions"][region]["dailies"]["recovered"][i - 1]
                            except:
                                self.countries[country]["regions"][region]["deltas"]["recovered"][i] = 0

                            self.countries[country]["regions"][region]["deltas"]["deaths"][i] = \
                                self.countries[country]["regions"][region]["dailies"]["deaths"][i] - \
                                self.countries[country]["regions"][region]["dailies"]["deaths"][i - 1]
                        else:
                            pass

                        # Set Country dailies
                        self.countries[country]["dailies"]["confirmed"][i] += daily_confirmed[i]
                        self.countries[country]["dailies"]["infected"][i] += daily_infected[i]
                        try:
                            self.countries[country]["dailies"]["recovered"][i] += daily_recovered[i]
                        except:
                            self.countries[country]["dailies"]["recovered"][i] += 0
                        self.countries[country]["dailies"]["deaths"][i] += daily_deaths[i]

                        self.countries[country]["deltas"]["confirmed"][i] += \
                        self.countries[country]["regions"][region]["deltas"]["confirmed"][i]
                        self.countries[country]["deltas"]["infected"][i] += \
                        self.countries[country]["regions"][region]["deltas"]["infected"][i]
                        self.countries[country]["deltas"]["recovered"][i] += \
                        self.countries[country]["regions"][region]["deltas"]["recovered"][i]
                        self.countries[country]["deltas"]["deaths"][i] += \
                        self.countries[country]["regions"][region]["deltas"]["deaths"][i]

                        # TODO: Keep going

                        # Add to overall dailies
                        total_daily_confirmed[i] += daily_confirmed[i]
                        total_daily_infected[i] += daily_infected[i]
                        try:
                            total_daily_recovered[i] += daily_recovered[i]
                        except:
                            total_daily_recovered[0] += 0

                        total_daily_deaths[i] += daily_deaths[i]

                    # if region == country:
                    #     del self.countries[country]["regions"][region]
                    # print(self.countries[country]["regions"][region]["deltas"]["confirmed"])
                # Set country totals
                self.countries[country]["totals"]["infected"] = infected
                self.countries[country]["totals"]["confirmed"] = confirmed
                self.countries[country]["totals"]["recovered"] = recovered
                self.countries[country]["totals"]["deaths"] = deaths

                for i in range(0, len(daily_confirmed)):
                    total_delta_confirmed[i] += self.countries[country]["deltas"]["confirmed"][i]
                    total_delta_infected[i] += self.countries[country]["deltas"]["infected"][i]
                    total_delta_recovered[i] += self.countries[country]["deltas"]["recovered"][i]
                    total_delta_deaths[i] += self.countries[country]["deltas"]["deaths"][i]

            total_confirmed += confirmed
            total_recovered += recovered
            total_infected += infected
            total_deaths += deaths

        new_us_regions = {}
        for region in self.countries['US']["regions"].keys():
            if len(region.split(", ")) == 1:
                new_us_regions.update({region: self.countries['US']["regions"][region]})
        #print(new_us_regions)
        self.countries['US']["regions"] = new_us_regions

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

        self.totals["deltas"] = {
            "confirmed": total_delta_confirmed,
            "infected": total_delta_infected,
            "recovered": total_delta_recovered,
            "deaths": total_delta_deaths,
        }

    def munge_csv_data(self, dataset):
        rows = []
        for row in dataset:
            rows.append(row)
        self.dates = rows[0][4:]
        rows = rows[1:len(rows) - 1]  # Fix for some weird row, maybe remove later
        return rows

    def gather_country_region_data(self, dataset, name):
        for row in dataset:
            region = row[0]
            country = row[1]
            if row[-1] == '':
                del row[-1]
            if region == '':
                region = country
            exclude = False
            # if country == 'US' and ", " in region:
            #     region = self.convert_region(region)
            if not exclude:
                try:
                    self.countries[country]["regions"][region]["totals"][name] = self.get_row_total(row)
                    self.countries[country]["regions"][region]["dailies"][name] = [int(x) for x in row[4:]]
                except:
                    pass
                

    def gather_infected(self):
        print("Gathering Infected...")
        for country_name, country in self.countries.items():
            if country_name == "China" and self.ignore_china:
                pass
            else:
                for region_name, region in country["regions"].items():
                    region_infected = 0
                    for i in range(0, self.date_count):
                        try:
                            region_infected = self.countries[country_name]["regions"][region_name]["dailies"]["confirmed"][
                                              i] - \
                                          self.countries[country_name]["regions"][region_name]["dailies"]["recovered"][
                                              i] - \
                                          self.countries[country_name]["regions"][region_name]["dailies"]["deaths"][i]
                        except:
                            region_infected = self.countries[country_name]["regions"][region_name]["dailies"]["confirmed"][
                                              i] - \
                                          self.countries[country_name]["regions"][region_name]["dailies"]["deaths"][i]
                        self.countries[country_name]["regions"][region_name]["dailies"]["infected"][i] = region_infected
                    self.countries[country_name]["regions"][region_name]["totals"]["infected"] = region_infected

    def get_row_total(self, row):
        row_total = row[-1]
        try:
            int_row_total = int(row[-1])
        except:
            int_row_total = 0
        try:
            return int(row_total)
        except:
            print(row)
            return 0

    def get_column_total(self, data, column_number):
        return sum([row[column_number] for row in data])

    def get_countries_regions(self):
        countries = {}
        for row in self.confirmed_time_series:
            country = row[1]
            region = row[0]
            if region == '':
                region = country
            exclude = False
            if not exclude:
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
                        "deltas": {
                            "confirmed": [0 for x in range(0, self.date_count)],
                            "infected": [0 for x in range(0, self.date_count)],
                            "recovered": [0 for x in range(0, self.date_count)],
                            "deaths": [0 for x in range(0, self.date_count)],
                        },
                        "regions": {}
                    }

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
                    },
                    "deltas": {
                        "confirmed": [0 for x in range(0, self.date_count)],
                        "infected": [0 for x in range(0, self.date_count)],
                        "recovered": [0 for x in range(0, self.date_count)],
                        "deaths": [0 for x in range(0, self.date_count)],
                    },
                }

        return countries

    @property
    def date_count(self):
        return len(self.dates)

    def dates_real(self):
        new_dates = []
        for date in self.dates:
            new_dates.append(datetime.datetime.strptime(date, "%m/%d/%y"))
        return new_dates

    def dates_iso(self):
        new_dates = []
        for date in self.dates_real():
            date_stamp = date.isoformat().split('.')[0] + 'Z'
            date_stamp = date_stamp.replace('T', ' ')
            new_dates.append(date_stamp)
        return new_dates