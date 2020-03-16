from flask import Flask, render_template, abort, jsonify
from analytics import Analytics
from load_data import DataLoader
import os
import numpy
from regression import exponential_regression
import config

APP = Flask(__name__)

URL_ATTRIBS = {
    "/": {
        "nav": "Worldwide Without China",
        "slug": "worldwide-minus",
        "title": "Covid-19 Worldwide Statistics (minus China)",
        "display_countries": True,
        "sub_levels": True
    },
    "/with-china": {
        "nav": "Worldwide including China",
        "slug": "worldwide",
        "title": "Covid-19 Worldwide (including China) Statistics",
        "display_countries": True,
        "sub_levels": True
    },
    "/minus-china": {
        "nav": "Worldwide Minus China",
        "slug": "worldwide-minus-china",
        "title": "Covid-19 Worldwide Statistics (minus China)",
        "display_countries": True,
        "sub_levels": True
    },
    "/growth": {
        "nav": "Growth",
        "slug": "growth",
        "title": "Covid-19 Growth Comarison",
        "display_countries": False,
        "sub_levels": False
    }
}

def convert_state_to_code(state):
    inv_map = {v: k for k, v in config.STATE_MAP.items()}
    if state in inv_map.keys():
        return inv_map[state].lower()
    else:
        return state.lower()

@APP.errorhandler(400)
def resource_not_found(e):
    return 'Our data provider is having issues and we will update as soon as possible', 400

@APP.errorhandler(500)
def resource_not_found(e):
    return 'Our data provider is having issues and we will update as soon as possible', 400

def create_js_compatible_date(date):
    d = date.split('/')
    return "gd(20" + d[2] + ", " + d[0] + ", " + d[1] + ")"


def render_page(url, minus_china, country_slug=None):
    url_prefix = os.getenv("URL_PREFIX")
    menu_data = config.WORLDWIDE_REGIONS
    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, minus_china)
    country_menu = config.COUNTRIES_MENU
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
                    if ', ' not in state:
                        adjusted_state = convert_state_to_code(state)
                        state_totals[adjusted_state] = 0
                for state, state_data in analytics.countries[country]["regions"].items():
                    if ', ' not in state:
                        adjusted_state = convert_state_to_code(state)
                        state_totals[adjusted_state] += analytics.countries[country]["regions"][state]["totals"]["confirmed"]
                        region_map_data[adjusted_state] = state_totals[adjusted_state]
                print(region_map_data)


            active_increased = True
            if primary_deltas['infected'] < 0:
                active_increased = False
        else:
            return abort(404, "Country not found")
    else:
        url_data = URL_ATTRIBS[url]
        totals = analytics.totals["totals"]
        print(analytics.totals["totals"])
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
                           date_stamp=data.update_date_stamp, menu_data=menu_data, region_map_data=region_map_data,
                           country_menu=country_menu)


@APP.route('/')
def homepage():
    return render_page(url='/', minus_china=True)


@APP.route('/minus-china')
def minus_china():
    return render_page(url='/minus-china', minus_china=True)

@APP.route('/with-china')
def with_china():
    return render_page(url='/with-china', minus_china=False)


@APP.route('/settings.html')
def settings():
    return render_template('settings.html')


@APP.route('/<country_slug>')
def render_country(country_slug):
    slug = country_slug.lower().replace(' ', '-')
    return render_page(url=None, minus_china=False, country_slug=slug)

@APP.route('/growth')
def compare_countries():
    url_data = URL_ATTRIBS['/growth']
    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, True)
    country_menu = config.COUNTRIES_MENU
    country_slugs = [x.lower().replace(' ', '-') for x in analytics.countries.keys()]
    country_slug_data = list(zip(country_slugs, analytics.countries.keys()))
    just_over_1000_countries = {}
    for country_name, country in analytics.countries.items():
        if country['totals']['confirmed'] > 2000:
            update = {
                country_name: country,
            }
            just_over_1000_countries.update(update)

    print(just_over_1000_countries)
    country_growths = {}
    max_days = 0
    chart_max = 25000

    country_count_over_1000 = 0

    for country_name, country in just_over_1000_countries.items():
        country_confirmed = []
        for day_count in country['dailies']['confirmed']:
            if day_count >= 100:
                country_confirmed.append(day_count)
                if day_count > chart_max:
                    chart_max = day_count
        if len(country_confirmed) > max_days:
            max_days = len(country_confirmed)
        if len(country_confirmed) > 0:
            country['growth'] = country_confirmed
            growths_update = {
                country_name: list(zip(range(0, len(country_confirmed)), country_confirmed))
            }
            country_growths.update(growths_update)

    final_data = []

    chart_steps = 0.50 / len(just_over_1000_countries.keys())
    country_growth_bars = {}
    index = 0
    country_count = len(country_growths.keys())
    for country_name, country_growth in country_growths.items():
        updated_growth = []
        for day in country_growth:
            day_value = day[0] + 0.25 + (chart_steps * index)
            updated_growth.append((day_value, day[1]))
        country_growth_bars[country_name] = updated_growth
        index += 1


    day_indexes = list(range(0, max_days))
    return render_template('compare.jinja2', country_growths=country_growths, url_data=url_data,
                           country_menu=country_menu, day_indexes=day_indexes, chart_max=chart_max,
                           date_stamp=data.update_date_stamp, country_growth_bars=country_growth_bars,
                           bar_width=chart_steps)