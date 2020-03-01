from flask import Flask, render_template

APP = Flask(__name__)

@APP.route('/')
def homepage():
    return render_template('dashboard.html')

@APP.route('/settings.html')
def settings():
    return render_template('settings.html')