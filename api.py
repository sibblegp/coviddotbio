from flask import Flask, render_template, abort, jsonify
import boto3
import json
import requests

API = Flask(__name__)


@API.route('/')
def homepage():
    s3 = boto3.resource('s3')
    analytics = requests.get("https://covidbio-covid-data.s3.us-east-2.amazonaws.com/analytics.json")
    # analytics_file = s3.Object('covidbio-covid-data', "analytics.json")
    # analytics_file_contents = analytics_file.get()['Body'].read()
    response = API.response_class(
        response=analytics.content.decode('utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response