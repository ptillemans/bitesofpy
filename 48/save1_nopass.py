import os
import re
import urllib.request
from collections import namedtuple
from itertools import groupby

LOG = os.path.join('/tmp', 'safari.logs')
PY_BOOK, OTHER_BOOK = '🐍', '.'
urllib.request.urlretrieve('http://bit.ly/2BLsCYc', LOG)

BOOK_PATTERN = re.compile("^(.*) - (.*)")
ACTION_PATTERN = re.compile("^- (\w*) (.*)")

Log = namedtuple('Log', 'date time user level message')
Book = namedtuple('Book', 'ts title')
Action = namedtuple('Action', 'type info')
Unknown = namedtuple("Unknown", 'msg')

def parse_message(msg):
    m = BOOK_PATTERN.match(msg)
    if m:
        return Book(m[1], m[3])
    m = ACTION_PATTERN.match(msg)
    if m:
        return Action(m[1].strip().lower(), m[2])
    return Unknown(msg)

def parse_line(line):
    (dt, tm, user, level, message) = line.split(maxsplit=4)
    return Log(dt, tm, user, level, message)
    
def read_log(filename):
    book = None
    with open(filename) as f:
        for line in f:
            yield parse_line(line)
        
def create_chart(): 
    for (date, daylog) in groupby(read_log(LOG), key = lambda l : l.date):
        bar = ''
        for info in (parse_message(l.message) for l in daylog):
            if isinstance(info, Book):
                book = Book
            if isinstance(info, Action):
                action = info
                if action.type == 'sending':
                    if 'python' in book.title.lower():
                        bar += PY_BOOK
                    else: 
                        bar += OTHER_BOOK
        
        print(f'{date} {bar}')
                    
        
            
    
        