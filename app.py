from flask import Flask, render_template, abort
from analytics import Analytics
from load_data import DataLoader
import os
import numpy
from regression import exponential_regression
import config

APP = Flask(__name__)

URL_ATTRIBS = {
    "/": {
        "nav": "Worldwide",
        "slug": "worldwide",
        "title": "Covid-19 Worldwide Statistics",
        "display_countries": True,
        "sub_levels": True
    },
    "/minus-china": {
        "nav": "Worldwide Minus China",
        "slug": "worldwide-minus-china",
        "title": "Covid-19 Worldwide Statistics Minus China",
        "display_countries": True,
        "sub_levels": True
    }
}


def create_js_compatible_date(date):
    d = date.split('/')
    return "gd(20" + d[2] + ", " + d[0] + ", " + d[1] + ")"


def render_page(url, minus_china, country_slug=None):
    url_prefix = os.getenv("URL_PREFIX")
    menu_data = config.WORLDWIDE_REGIONS
    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, minus_china)

    country_slugs = [x.lower().replace(' ', '-') for x in analytics.countries.keys()]
    country_slug_data = list(zip(country_slugs, analytics.countries.keys()))

    deltas_timeseries = {
        "confirmed": [0],
        "infected": [0],
        "recovered": [0],
        "deaths": [0]
    }

    country_pairs = {}
    region_map_data = {}
    for pair in country_slug_data:
        country_pairs.update({pair[0]: pair[1]})
    if country_slug:
        if country_slug in country_slugs:
            country = country_pairs[country_slug]
            totals = analytics.countries[country]['totals']

            region_display = False
            countries = []
            if 'regions' in analytics.countries[country]:
                region_display = True
                countries = analytics.countries[country]["regions"]

            url_data = {
                "nav": country,
                "slug": country.lower(),
                "title": country + " Statistics",
                "display_countries": False,
                "sub_levels": region_display
            }
            chart_data = {
                "confirmed": list(zip(analytics.dates, analytics.countries[country]["dailies"]["confirmed"])),
                "recovered": list(zip(analytics.dates, analytics.countries[country]["dailies"]["recovered"])),
                "deaths": list(zip(analytics.dates, analytics.countries[country]["dailies"]["deaths"])),
                "infected": list(zip(analytics.dates, analytics.countries[country]["dailies"]["infected"]))
            }

            for i in range(1, analytics.date_count):
                confirmed_delta = int(analytics.countries[country]["dailies"]["confirmed"][i]) - int(analytics.countries[country]["dailies"]["confirmed"][i - 1])
                recovered_delta = int(analytics.countries[country]["dailies"]["recovered"][i]) - int(
                    analytics.countries[country]["dailies"]["recovered"][i - 1])
                infected_delta = int(analytics.countries[country]["dailies"]["infected"][i]) - int(
                    analytics.countries[country]["dailies"]["infected"][i - 1])
                deaths_delta = int(analytics.countries[country]["dailies"]["deaths"][i]) - int(
                    analytics.countries[country]["dailies"]["deaths"][i - 1])


                deltas_timeseries["confirmed"].append(confirmed_delta)
                deltas_timeseries["infected"].append(infected_delta)
                deltas_timeseries["recovered"].append(recovered_delta)
                deltas_timeseries["deaths"].append(deaths_delta)

            delta_chart_data = {
                "confirmed": list(zip(analytics.dates, deltas_timeseries["confirmed"])),
                "recovered": list(zip(analytics.dates, deltas_timeseries["recovered"])),
                "deaths": list(zip(analytics.dates, deltas_timeseries["deaths"])),
                "infected": list(zip(analytics.dates, deltas_timeseries["infected"]))
            }


            primary_deltas = {
                "confirmed": analytics.countries[country]["deltas"]["confirmed"][-1],
                "recovered": analytics.countries[country]["deltas"]["recovered"][-1],
                "deaths": analytics.countries[country]["deltas"]["deaths"][-1],
                "infected": analytics.countries[country]["deltas"]["infected"][-1],
            }

            regression_data = {
                "confirmed": exponential_regression(range(0, analytics.date_count),
                                                    analytics.countries[country]["dailies"]["confirmed"])
            }

            if country_slug == 'us':
                state_totals = {}
                for state in analytics.countries[country]["regions"].keys():
                    if ', ' in state:
                        state_name = state.split(', ')[1].split(' ')[0].lower()
                        state_totals[state_name] = 0
                for state, state_data in analytics.countries[country]["regions"].items():
                    if ', ' in state:
                        state_name = state.split(', ')[1].split(' ')[0].lower()
                        state_totals[state_name] += analytics.countries[country]["regions"][state]["totals"]["confirmed"]
                        region_map_data[state_name] = state_totals[state_name]
                print(region_map_data)


            active_increased = True
            if primary_deltas['infected'] < 0:
                active_increased = False
        else:
            return abort(404, "Country not found")
    else:
        url_data = URL_ATTRIBS[url]
        totals = analytics.totals["totals"]
        chart_data = {
            "confirmed": list(zip(analytics.dates, analytics.totals["dailies"]["confirmed"])),
            "recovered": list(zip(analytics.dates, analytics.totals["dailies"]["recovered"])),
            "deaths": list(zip(analytics.dates, analytics.totals["dailies"]["deaths"])),
            "infected": list(zip(analytics.dates, analytics.totals["dailies"]["infected"])),
        }

        primary_deltas = {
            "confirmed": analytics.totals["deltas"]["confirmed"][-1],
            "recovered": analytics.totals["deltas"]["recovered"][-1],
            "deaths": analytics.totals["deltas"]["deaths"][-1],
            "infected": analytics.totals["deltas"]["infected"][-1],
        }

        for i in range(1, analytics.date_count):
            confirmed_delta = int(analytics.totals["dailies"]["confirmed"][i]) - int(
                analytics.totals["dailies"]["confirmed"][i - 1])
            recovered_delta = int(analytics.totals["dailies"]["recovered"][i]) - int(
                analytics.totals["dailies"]["recovered"][i - 1])
            infected_delta = int(analytics.totals["dailies"]["infected"][i]) - int(
                analytics.totals["dailies"]["infected"][i - 1])
            deaths_delta = int(analytics.totals["dailies"]["deaths"][i]) - int(
                analytics.totals["dailies"]["deaths"][i - 1])

            deltas_timeseries["confirmed"].append(confirmed_delta)
            deltas_timeseries["infected"].append(infected_delta)
            deltas_timeseries["recovered"].append(recovered_delta)
            deltas_timeseries["deaths"].append(deaths_delta)

        delta_chart_data = {
            "confirmed": list(zip(analytics.dates, deltas_timeseries["confirmed"])),
            "recovered": list(zip(analytics.dates, deltas_timeseries["recovered"])),
            "deaths": list(zip(analytics.dates, deltas_timeseries["deaths"])),
            "infected": list(zip(analytics.dates, deltas_timeseries["infected"]))
        }

        regression_data = {
            "confirmed": exponential_regression(range(0, analytics.date_count), analytics.totals["dailies"]["confirmed"])
        }


        # print(analytics.totals["deltas"])
        # print(analytics.countries["South Korea"]["deltas"])
        # print(analytics.countries["Mainland China"]["deltas"])

        active_increased = True
        if primary_deltas['infected'] < 0:
            active_increased = False
        countries = analytics.countries

    trend_chart_data = {"confirmed": list(zip(analytics.dates, regression_data["confirmed"]))}

    dates = analytics.dates
    return render_template('dashboard.jinja2', chart_data=chart_data, totals=totals,
                           primary_deltas=primary_deltas, countries=countries, url_data=url_data, url_prefix=url_prefix,
                           active_increased=active_increased, dates=dates, trend_chart_data=trend_chart_data,
                           delta_chart_data=delta_chart_data, update_string=data.update_string,
                           date_stamp=data.update_date_stamp, menu_data=menu_data, region_map_data=region_map_data)


@APP.route('/')
def homepage():
    return render_page(url='/', minus_china=False)


@APP.route('/minus-china')
def minus_china():
    return render_page(url='/minus-china', minus_china=True)


@APP.route('/settings.html')
def settings():
    return render_template('settings.html')


@APP.route('/<country_slug>')
def render_country(country_slug):
    slug = country_slug.lower().replace(' ', '-')
    return render_page(url=None, minus_china=False, country_slug=slug)
