from flask import Flask, render_template, abort
from analytics import Analytics
from load_data import DataLoader
import os
APP = Flask(__name__)

URL_ATTRIBS = {
    "/": {
        "nav": "Worldwide",
        "slug": "worldwide",
        "title": "Covid-19 Worldwide Statistics",
        "display_countries": True
    },
    "/minus-china": {
        "nav": "Worldwide Minus China",
        "slug": "worldwide-minus-china",
        "title": "Covid-19 Worldwide Statistics Minus China",
        "display_countries": True
    }
}

def create_js_compatible_date(date):
    d = date.split('/')
    return "gd(20" + d[2] + ", " + d[0] + ", " + d[1] +")"

def render_page(url, minus_china, country_slug=None):
    url_prefix = os.getenv("URL_PREFIX")

    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, minus_china)

    country_slugs = [x.lower().replace(' ', '-') for x in analytics.countries.keys()]
    country_slug_data = list(zip(country_slugs, analytics.countries.keys()))

    country_pairs = {}
    for pair in country_slug_data:
        country_pairs.update({pair[0]: pair[1]})
    if country_slug:
        if country_slug in country_slugs:
            country = country_pairs[country_slug]
            totals = analytics.countries[country]['totals']
            url_data = {
                "nav": country,
                "slug": country.lower(),
                "title": country + " Statistics",
                "display_countries": False
            }
            chart_data = {
                "confirmed": list(zip(analytics.dates, analytics.countries[country]["dailies"]["confirmed"])),
                "recovered": list(zip(analytics.dates, analytics.countries[country]["dailies"]["recovered"])),
                "deaths": list(zip(analytics.dates, analytics.countries[country]["dailies"]["deaths"])),
                "infected": list(zip(analytics.dates, analytics.countries[country]["dailies"]["infected"]))
            }

            primary_deltas = {
                "confirmed": analytics.countries[country]["deltas"]["confirmed"][-1],
                "recovered": analytics.countries[country]["deltas"]["recovered"][-1],
                "deaths": analytics.countries[country]["deltas"]["deaths"][-1],
                "infected": analytics.countries[country]["deltas"]["infected"][-1],
            }

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

        # print(analytics.totals["deltas"])
        # print(analytics.countries["South Korea"]["deltas"])
        # print(analytics.countries["Mainland China"]["deltas"])

        active_increased = True
        if primary_deltas['infected'] < 0:
            active_increased = False

    countries = analytics.countries
    dates = analytics.dates
    return render_template('dashboard.jinja2', chart_data=chart_data, totals=totals,
                               primary_deltas=primary_deltas, countries=countries, url_data=url_data, url_prefix=url_prefix,
                               active_increased=active_increased, dates=dates)

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