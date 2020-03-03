import datetime
from hashlib import sha256
import boto3
import requests

from load_data import DataLoader

def get_files():
    s3 = boto3.resource('s3')
    confirmed_file = s3.Object('covidbio-covid-data', "confirmed.csv")
    confirmed_file_contents = confirmed_file.get()['Body'].read()
    confirmed_file_sha = sha256(confirmed_file_contents).hexdigest()

    data = DataLoader(live=True)

    downloaded_confirmed_sha = sha256(data.confirmed.content).hexdigest()
    if confirmed_file_sha == downloaded_confirmed_sha: #TODO: Make this not equal

        s3.Bucket('covidbio-covid-data').put_object(Key='confirmed.csv', Body=data.confirmed.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='recovered.csv', Body=data.recovered.content.decode('utf-8'),
                                                    ACL='public-read')
        s3.Bucket('covidbio-covid-data').put_object(Key='deaths.csv', Body=data.deaths.content.decode('utf-8'),
                                                    ACL='public-read')
        date_string = datetime.datetime.utcnow().strftime('Last updated on %B %d, %Y at %H:%M UTC')
        s3.Bucket('covidbio-covid-data').put_object(Key='updated_string.txt', Body=date_string, ACL='public-read')