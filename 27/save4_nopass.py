import glob
import json
import os
import re
from pprint import pprint
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/omdb/'
MOVIES = ('bladerunner2049 fightclub glengary '
          'horrible-bosses terminator').split()
TMP = '/tmp'

# little bit of prework (yes working on pip installables ...)
for movie in MOVIES:
    fname = f'{movie}.json'
    remote = os.path.join(BASE_URL, fname)
    local = os.path.join(TMP, fname)
    urlretrieve(remote, local)

files = glob.glob(os.path.join(TMP, '*json'))


def get_movie_data(files=files):
    return [json.load(open(f)) 
            for f in files]


def get_single_comedy(movies):
    matches = [movie 
      for movie in movies
      if 'comedy' in movie['Genre'].lower()
    ]
    return matches[0]['Title']


def get_movie_most_nominations(movies):
    def get_nominations(movie):
        awards = movie['Awards']
        noms = re.match(r'.* (\d+) nominations.', awards)[1]
        if noms:
            return int(noms)
        else:
            return -1
        
    movies.sort(key=get_nominations, reverse=True)
    return movies[0]['Title']


def get_movie_longest_runtime(movies):
    def get_runtime(movie):
        runtime = movie['Runtime']
        mins = re.match(r'(\d+) min.*', runtime)[1]
        if mins:
            return int(mins)
        else:
            return -1
            
    movies.sort(key=get_runtime)
    return movies[0]['Title']
    
    
    
movies = get_movie_data(files)

pprint(get_movie_longest_runtime(movies))