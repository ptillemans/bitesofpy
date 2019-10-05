import os
import urllib.request
import string
from collections import Counter

# data provided
stopwords_file = os.path.join('/tmp', 'stopwords')
harry_text = os.path.join('/tmp', 'harry')
urllib.request.urlretrieve('http://bit.ly/2EuvyHB', stopwords_file)
urllib.request.urlretrieve('http://bit.ly/2C6RzuR', harry_text)

with open(stopwords_file) as f:
    stopwords = [line.strip() for line in f]
print(stopwords)

def clean_word(word):
    cleaned = [c for c in word.strip().lower() if c in string.ascii_letters]
    return ''.join(cleaned)
    
def clean_words(f):
    return [clean_word(word) 
                           for line in f
                           for raw in line.split(' ')
                           for word in [clean_word(raw)]
                           if word not in stopwords]
                           
def get_harry_most_common_word():
    
    with open(harry_text) as f:
        words = clean_words(f)
    counter = Counter(words)
    print(counter)
    return counter.most_common()[0]