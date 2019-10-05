import os
from collections import Counter
import urllib.request
import xml.etree.ElementTree as ET

# prep
tempfile = os.path.join('/tmp', 'feed')
urllib.request.urlretrieve('http://bit.ly/2zD8d8b', tempfile)

with open(tempfile) as f:
    content = f.read().lower()


# start coding

def get_pybites_top_tags(n=10):
    """use Counter to get the top 10 PyBites tags from the feed
       data already loaded into the content variable"""
    root = ET.fromstring(content)
    counter = Counter([e.text() from e in root.findall('category')])
    return counter.most_common(n)