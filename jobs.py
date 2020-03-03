import boto3
import requests

from load_data import DataLoader

def get_files():
    data = DataLoader(live=True)

    s3 = boto3.resource('s3')
    s3.Bucket('covidbio-covid-data').put_object(Key='confirmed.csv', Body=data.confirmed.content.decode('utf-8'),
                                                ACL='public-read')
    s3.Bucket('covidbio-covid-data').put_object(Key='recovered.csv', Body=data.recovered.content.decode('utf-8'),
                                                ACL='public-read')
    s3.Bucket('covidbio-covid-data').put_object(Key='deaths.csv', Body=data.deaths.content.decode('utf-8'),
                                                ACL='public-read')