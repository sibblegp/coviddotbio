import datetime
from hashlib import sha256
import boto3
import json
import copy
from analytics import Analytics
import datetime

from load_data import DataLoader

def get_files():
    s3 = boto3.resource('s3')
    confirmed_file = s3.Object('covidbio-covid-data', "confirmed.csv")
    confirmed_file_contents = confirmed_file.get()['Body'].read()
    confirmed_file_sha = sha256(confirmed_file_contents).hexdigest()

    data = DataLoader(live=True)
    data2 = DataLoader(live=True)
    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, data.us_cases_raw, data.us_deaths_raw, ignore_china=False)
    analytics_without_china = Analytics(data2.confirmed_raw, data2.recovered_raw, data2.deaths_raw, data.us_cases_raw, data.us_deaths_raw, ignore_china=True)

    #TODO: Check the data here

    downloaded_confirmed_sha = sha256(data.confirmed.content).hexdigest()
    if confirmed_file_sha != downloaded_confirmed_sha:

        s3.Bucket('covidbio-covid-data').put_object(Key='confirmed.csv', Body=data.confirmed.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='recovered.csv', Body=data.recovered.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='deaths.csv', Body=data.deaths.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='us_cases.csv', Body=data.us_cases.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='us_deaths.csv', Body=data.us_deaths.content.decode('utf-8'),
                                                    ACL='public-read')
        date_string = datetime.datetime.utcnow().strftime('Last updated on %B %d, %Y at %H:%M UTC')
        date_stamp = datetime.datetime.utcnow().isoformat().split('.')[0] + 'Z'
        date_stamp = date_stamp.replace('T', ' ')
        s3.Bucket('covidbio-covid-data').put_object(Key='updated_string.txt', Body=date_string, ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='date_stamp.txt', Body=date_stamp, ACL='public-read')


def publish_analytics():
    data = DataLoader(live=True)

    data2 = DataLoader(live=True)

    analytics = Analytics(data.confirmed_raw, data.recovered_raw, data.deaths_raw, data.us_cases_raw, data.us_deaths_raw, ignore_china=False)
    analytics_without_china = Analytics(data2.confirmed_raw, data2.recovered_raw, data2.deaths_raw, data.us_cases_raw, data.us_deaths_raw, ignore_china=True)

    date_stamp = datetime.datetime.utcnow().isoformat().split('.')[0] + 'Z'
    date_stamp = date_stamp.replace('T', ' ')

    s3 = boto3.resource('s3')
    full_dates = analytics.dates_iso()
    json_data = {
        "updated_at": date_stamp,
        "time-series-dates": full_dates,
        "totals": analytics.totals,
        "totals-minus-china": analytics_without_china.totals,
        "countries": analytics.countries,
        "raw-dates": analytics.dates,
        "date-string": data.update_string,
        "date-stamp": data.update_date_stamp
    }

    s3.Bucket('covidbio-covid-data').put_object(Key='analytics.json', Body=json.dumps(json_data),
                                                ACL='public-read')
