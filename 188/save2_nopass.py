from os import path
import statistics as st
from urllib.request import urlretrieve


STATS = path.join('/tmp', 'testfiles_number_loc.txt')
if not path.isfile(STATS):
    urlretrieve('https://bit.ly/2Jp5CUt', STATS)

STATS_OUTPUT = """
Basic statistics:
- count     : {count:7d}
- min       : {min_:7d}
- max       : {max_:7d}
- mean      : {mean:7.2f}

Population variance:
- pstdev    : {pstdev:7.2f}
- pvariance : {pvariance:7.2f}

Estimated variance for sample:
- count     : {sample_count:7.2f}
- stdev     : {sample_stdev:7.2f}
- variance  : {sample_variance:7.2f}
"""


def get_all_line_counts(data: str = STATS) -> list:
    """Get all 186 line counts from the STATS file,
       returning a list of ints"""
    # TODO 1: get the 186 ints from downloaded STATS file
    with open(STATS) as f:
        counts = [int(line.split(' ')[0]) for line in f]
        
    return list(counts)


def create_stats_report(data=None):
    if data is None:
        # converting to a list in case a generator was returned
        data = list(get_all_line_counts())

    # taking a sample for the last section
    sample = list(data)[::2]

    # TODO 2: complete this dict, use data list and
    # for the last 3 sample_ variables, use sample list
    stats = dict(count=count(data),
                 min_=min(data),
                 max_=max(data),
                 mean=mean(data),
                 pstdev=pstdev(data),
                 pvariance=pvariance(data),
                 sample_count=count(sample),
                 sample_stdev=stdev(sample),
                 sample_variance=variance(sample),
                 )

    return STATS_OUTPUT.format(**stats)