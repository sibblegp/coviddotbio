from flask import Flask, render_template
from analytics import Analytics
from load_data import DataLoader
APP = Flask(__name__)

def create_js_compatible_date(date):
    d = date.split('/')
    return "gd(20" + d[2] + ", " + d[0] + ", " + d[1] +")"

@APP.route('/')
def homepage():
    data = DataLoader()
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, True)

    chart_data = {
        "confirmed": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["confirmed"])),
        "recovered": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["recovered"])),
        "deaths": list(zip(range(0, len(analytics.dates)), analytics.totals["dailies"]["deaths"]))
    }
    return render_template('dashboard.jinja2', chart_data=chart_data, totals=analytics.totals["totals"])

@APP.route('/settings.html')
def settings():
    return render_template('settings.html')