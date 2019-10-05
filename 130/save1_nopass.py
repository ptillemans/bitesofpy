from collections import Counter

import requests

CAR_DATA = 'https://bit.ly/2Ov65SJ'

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(CAR_DATA).json()


# your turn:
def most_prolific_automaker(year):
    """Given year 'year' return the automaker that released
       the highest number of new car models"""
    models = [ r['automaker'] for r in data if r['year'] == year ]
    model_counts = Counter(models).most_common()
    return model_counts[0]

def get_models(automaker, year):
    """Filter cars 'data' by 'automaker' and 'year',
       return a set of models (a 'set' to avoid duplicate models)"""
    models = { r['model'] for r in data 
               if r['automaker'] == automaker and r['year'] == year}