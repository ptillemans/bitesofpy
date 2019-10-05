import csv
from collections import defaultdict, namedtuple
import os
import statistics
from urllib.request import urlretrieve
from pprint import pprint

BASE_URL = 'http://projects.bobbelderbos.com/pcc/movies/'
TMP = '/tmp'

fname = 'movie_metadata.csv'
remote = os.path.join(BASE_URL, fname)
local = os.path.join(TMP, fname)
urlretrieve(remote, local)

MOVIE_DATA = local
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    movies = {}
    with open(local) as f:
        reader = csv.DictReader(f)
        for movie in reader:
            director = movie['director_name']
            title = movie['movie_title']
            year = movie['title_year']
            score = float(movie['imdb_score'])
            
            ms = movies.get(director,[])
            ms.append(Movie(title, year, score))
            movies[director] = ms
            
    return movies


def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    mean = statistics.mean([movie.score for movie in movies])
    return round(mean, 1)


def get_average_scores(directors):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    scored_movies [
        (director, calc_mean_score(movies))
        for (director, movies) in directors.items()
        if len(movies) >= MIN_MOVIES
    ]
    
    scored_movies.sort(key=lambda (_, score): score, reverse=True)
    return scored_movies
    
movies = get_movies_by_director()
pprint(get_average_scores(movies))
    