from collections import Counter
import os
from datetime import datetime
from urllib.request import urlretrieve
from collections import Counter
import re
from pprint import pprint

from dateutil.parser import parse

commits = os.path.join('/tmp', 'commits')
urlretrieve('https://bit.ly/2H1EuZQ', commits)

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'

def parse_line(line) -> (datetime, int):
    """
    Parse a log line and return a tuple with the
    (date, #inserts + #deletes)
    """
    raw_date, message = line.split(" | ")
    date = datetime.strptime(raw_date, "Date:   %c %z")
    activity = 0
    m = re.match(".*(\d+) insert.*", message)
    if m:
        activity += int(m[1])
    m = re.match(".*(\d+) delet.*", message)
    if m:
        activity += int(m[1])
    return (date, activity)
    
def read_log(fname: str):
    with open(fname) as f:
        for line in f:
            yield parse_line(line)
    
def get_min_max_amount_of_commits(commit_log: str = commits,
                                  year: int = None) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    act_cnt = Counter()
    for date, activity in read_log(commit_log):
        if year and year != date.year:
            pass
        else:
            month = date.strftime("%Y-%m")
            act_cnt[month] += activity
            
    ranking = act_cnt.most_common()
    pprint(ranking)
    return(ranking[-1][0], ranking[0][0])
    
    
    
    