import csv
from pathlib import Path
from urllib.request import urlretrieve
from itertools import islice
import re
from pprint import pprint

tmp = Path('/tmp')
stats = tmp / 'bites.csv'

if not stats.exists():
    urlretrieve('https://bit.ly/2MQyqXQ', stats)


def _parse_difficulty(row):
    s = row['Difficulty']
    if s == 'None':
        return 0.0
    else:
        return float(s)
        
def _parse_bite(row):
    s = row['Bite']
    m = re.match("Bite (\d+) ",s)
    return m[1]
        
def get_most_complex_bites(N=10, stats=stats):
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    with open(stats, encoding="utf-8-sig") as f:
        bites = list(csv.DictReader(f, delimiter=';'))
    
    bites.sort(key=_parse_difficulty, reverse=True)
    
    bite_names = (_parse_bite(bite) for bite in bites)
    return list(islice(bite_names, N))


if __name__ == '__main__':
    res = get_most_complex_bites()
    print(res)