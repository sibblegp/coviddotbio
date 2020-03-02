from flask import Flask, render_template
from analytics import Analytics
from load_data import DataLoader
APP = Flask(__name__)

URL_ATTRIBS = {
    "/": {
        "nav": "Worldwide",
        "slug": "worldwide",
        "title": "Covid-19 Worldwide Statistics"
    },
    "/minus-china": {
        "nav": "Worldwide Minus China",
        "slug": "worldwide-minus-china",
        "title": "Covid-19 Worldwide Statistics Minus China"
    }
}

def create_js_compatible_date(date):
    d = date.split('/')
    return "gd(20" + d[2] + ", " + d[0] + ", " + d[1] +")"

def render_page(url, minus_china):

    url_data = URL_ATTRIBS[url]
    print(url_data)

    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, minus_china)

    chart_data = {
        "confirmed": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["confirmed"])),
        "recovered": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["recovered"])),
        "deaths": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["deaths"]))
    }

    primary_deltas = {
        "confirmed": analytics.totals["deltas"]["confirmed"][-1],
        "recovered": analytics.totals["deltas"]["recovered"][-1],
        "deaths": analytics.totals["deltas"]["deaths"][-1],
        "infected": analytics.totals["deltas"]["infected"][-1],
    }

    countries = analytics.countries
    return render_template('dashboard.jinja2', chart_data=chart_data, totals=analytics.totals["totals"],
                           primary_deltas=primary_deltas, countries=countries, url_data=url_data)

@APP.route('/')
def homepage():
    return render_page(url='/', minus_china=False)

@APP.route('/minus-china')
def minus_china():
    return render_page(url='/minus-china', minus_china = True)

@APP.route('/settings.html')
def settings():
    return render_template('settings.html')