import csv
from collections import Counter
import requests

CSV_URL = 'https://bit.ly/2HiD2i8'


def get_csv():
    """Use requests to download the csv and return the
       decoded content"""
    response = requests.get(CSV_URL)
    return csv.DictReader(response.text.splitlines())


def create_user_bar_chart(content):
    """Receives csv file (decoded) content and returns a table of timezones
       and their corresponding member counts in pluses (see Bite/tests)"""
    community = Counter([d['tz'] for d in content])
    tzs = sorted(community.keys())
    for tz in tzs:
       print(f"{tz:20} | {'+' * community[tz]}")