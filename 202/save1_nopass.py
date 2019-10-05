import csv
from pathlib import Path
from urllib.request import urlretrieve
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
        
def get_most_complex_bites(N=10, stats=stats):
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    with open(stats) as f:
        bites = list(csv.DictReader(f, delimiter=';'))
    
    pprint(bites)
    
    bites.sort(key=_parse_difficulty, reverse=True)
    
    return [bites[i]['Bite'] for i in range(N)]


if __name__ == '__main__':
    res = get_most_complex_bites()
    print(res)