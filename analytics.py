from config import STATE_MAP
import datetime

class Analytics:

    def __init__(self, confirmed_raw, recovered_raw, deaths_raw, us_cases, us_deaths, ignore_china=False):
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
        self.us_cases_raw = us_cases
        self.us_deaths_raw = us_deaths
        self.primary_data = None
        self.dates = []
        self.confirmed_time_series = self.munge_csv_data(self.confirmed_raw)
        self.recovered_time_series = self.munge_csv_data(self.recovered_raw)
        self.deaths_time_series = self.munge_csv_data(self.deaths_raw)
        self.us_confirmed_time_series = self.munge_csv_data(self.us_cases_raw, True)
        self.us_deaths_time_series = self.munge_csv_data(self.us_deaths_raw, True)
        self.countries = self.get_countries_regions()
        self.states = self.get_states()

        self.gather_country_region_data(self.confirmed_time_series, "confirmed")
        self.gather_country_region_data(self.recovered_time_series, "recovered")
        self.gather_country_region_data(self.deaths_time_series, "deaths")
        self.gather_us_county_region_data(self.us_confirmed_time_series, "confirmed")
        self.gather_us_county_region_data(self.us_deaths_time_series, "deaths")
        #self.gather_infected()

        self.totals = {}
        self.set_country_totals(self.countries)
        self.set_country_totals(self.states, False)
        self.countries['US']['regions'] = self.states
        # print(self.countries["China"])

    def convert_region(self, region, country):
        new_region = region
        region_parts = region.split(", ")
        if len(region_parts) > 1 and country == 'US':
            new_region = STATE_MAP[region_parts[1].strip()]
        return new_region

    def set_country_totals(self, data, is_total_data=True):
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
        for country in data.keys():
            infected = 0
            confirmed = 0
            recovered = 0
            deaths = 0
            if country == "China" and self.ignore_china:
                pass
            else:
                for region in data[country]["regions"].keys():
                    # Add to overall totals
                    adjusted_region = self.convert_region(region, country)
                    infected += data[country]["regions"][region]["totals"]["infected"]
                    confirmed += data[country]["regions"][region]["totals"]["confirmed"]
                    recovered += data[country]["regions"][region]["totals"]["recovered"]
                    deaths += data[country]["regions"][region]["totals"]["deaths"]

                    # Add to region dailies
                    daily_confirmed = data[country]["regions"][region]["dailies"]["confirmed"]
                    daily_infected = data[country]["regions"][region]["dailies"]["infected"]
                    daily_recovered = data[country]["regions"][region]["dailies"]["recovered"]
                    daily_deaths = data[country]["regions"][region]["dailies"]["deaths"]

                    for i in range(0, len(daily_confirmed)):
                        # Set region deltas
                        if i != 0:
                            data[country]["regions"][region]["deltas"]["confirmed"][i] = \
                            data[country]["regions"][region]["dailies"]["confirmed"][i] - \
                            data[country]["regions"][region]["dailies"]["confirmed"][i - 1]

                            data[country]["regions"][region]["deltas"]["infected"][i] = \
                                data[country]["regions"][region]["dailies"]["infected"][i] - \
                                data[country]["regions"][region]["dailies"]["infected"][i - 1]

                            try:
                                data[country]["regions"][region]["deltas"]["recovered"][i] = \
                                    data[country]["regions"][region]["dailies"]["recovered"][i] - \
                                    data[country]["regions"][region]["dailies"]["recovered"][i - 1]
                            except:
                                data[country]["regions"][region]["deltas"]["recovered"][i] = 0

                            data[country]["regions"][region]["deltas"]["deaths"][i] = \
                                data[country]["regions"][region]["dailies"]["deaths"][i] - \
                                data[country]["regions"][region]["dailies"]["deaths"][i - 1]
                        else:
                            pass

                        # Set Country dailies
                        data[country]["dailies"]["confirmed"][i] += daily_confirmed[i]
                        data[country]["dailies"]["infected"][i] += daily_infected[i]
                        try:
                            data[country]["dailies"]["recovered"][i] += daily_recovered[i]
                        except:
                            data[country]["dailies"]["recovered"][i] += 0
                        data[country]["dailies"]["deaths"][i] += daily_deaths[i]

                        data[country]["deltas"]["confirmed"][i] += \
                        data[country]["regions"][region]["deltas"]["confirmed"][i]
                        data[country]["deltas"]["infected"][i] += \
                        data[country]["regions"][region]["deltas"]["infected"][i]
                        data[country]["deltas"]["recovered"][i] += \
                        data[country]["regions"][region]["deltas"]["recovered"][i]
                        data[country]["deltas"]["deaths"][i] += \
                        data[country]["regions"][region]["deltas"]["deaths"][i]

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
                    #     del data[country]["regions"][region]
                    # print(data[country]["regions"][region]["deltas"]["confirmed"])
                # Set country totals
                data[country]["totals"]["infected"] = infected
                data[country]["totals"]["confirmed"] = confirmed
                data[country]["totals"]["recovered"] = recovered
                data[country]["totals"]["deaths"] = deaths

                for i in range(0, len(daily_confirmed)):
                    total_delta_confirmed[i] += data[country]["deltas"]["confirmed"][i]
                    total_delta_infected[i] += data[country]["deltas"]["infected"][i]
                    total_delta_recovered[i] += data[country]["deltas"]["recovered"][i]
                    total_delta_deaths[i] += data[country]["deltas"]["deaths"][i]

            total_confirmed += confirmed
            total_recovered += recovered
            total_infected += infected
            total_deaths += deaths

        if is_total_data:

            new_us_regions = {}
            for region in self.countries['US']["regions"].keys():
                if len(region.split(", ")) == 1:
                    new_us_regions.update({region: data['US']["regions"][region]})
            # print(new_us_regions)
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
        return data

    def munge_csv_data(self, dataset, us=False):
        rows = []
        for row in dataset:
            rows.append(row)
        if not us:
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

    def gather_us_county_region_data(self, dataset, name):
        for row in dataset:
            county = row[5]
            state = row[6]
            print(county + state)
            if row[-1] == '':
                del row[-1]
            if county == '':
                county = state
            exclude = False
            # if country == 'US' and ", " in region:
            #     region = self.convert_region(region)
            if not exclude:
                if state != '' and county != '':
                    self.states[state]['regions'][county]["totals"][name] = self.get_row_total(row)
                    self.states[state]['regions'][county]["dailies"][name] = [int(x) for x in row[11:]]
                

    def gather_infected(self):
        print("Gathering Infected...")
        for country_name, country in self.countries.items():
            if country_name == "China" and self.ignore_china:
                pass
            else:
                for region_name, region in country["regions"].items():
                    region_infected = 0
                    print(country_name + region_name)
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

    def get_states(self):
        states = {}
        for row in self.us_confirmed_time_series:
            state = row[6]
            county = row[5]
            print(state + county)
            if county == '':
                county = state
            exclude = False
            if not exclude:
                if state not in states:
                    states[state] = {
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

                states[state]["regions"][county] = {
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

        return states


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