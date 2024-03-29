from collections import Counter, defaultdict
import csv
from io import StringIO
from pprint import pprint

import requests

CSV_URL = 'https://raw.githubusercontent.com/pybites/SouthParkData/master/by-season/Season-{}.csv' # noqa E501


def get_season_csv_file(season):
    """Receives a season int, and downloads loads in its
       corresponding CSV_URL"""
    with requests.Session() as s:
        download = s.get(CSV_URL.format(season))
        return download.content.decode('utf-8')


def get_num_words_spoken_by_character_per_episode(content):
    """Receives loaded csv content (str) and returns a dict of
       keys=characters and values=Counter object,
       which is a mapping of episode=>words spoken"""
    result = defaultdict(Counter)
    
    with StringIO(content) as f:
        for line in csv.DictReader(f):
            pprint(line)
            c = result[line['Character']]
            c[line['Episode']] += len(line['Line'].split())
        
    return result