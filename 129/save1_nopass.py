import requests

STOCK_DATA = 'https://bit.ly/2MzKAQg'

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(STOCK_DATA).json()


# your turn:

def _cap_str_to_mln_float(cap):
    """If cap = 'n/a' return 0, else:
       - strip off leading '$',
       - if 'M' in cap value, strip it off and return value as float,
       - if 'B', strip it off and multiple by 1,000 and return
         value as float"""
    if cap == 'n/a':
        return 0
        
    cap = cap.strip('$')
    if 'M' in cap:
        return float(cap.strip('M'))
    elif 'B' in cap:
        return 1000 * float(cap.strip('B'))
    else:
        raise ValueError("Unsupported cap value : " + cap)
        


def get_industry_cap(industry):
    """Return the sum of all cap values for given industry, use
       the _cap_str_to_mln_float to parse the cap values,
       return a float with 2 digit precision"""
    total = sum((_cap_str_to_mln_float(s['cap'])
      for s in data
      if s['industry'] == industry
    ))
    return round(total, 2)

def get_stock_symbol_with_highest_cap():
    """Return the stock symbol (e.g. PACD) with the highest cap, use
       the _cap_str_to_mln_float to parse the cap values"""
    stock = max(data, key=lambda s: _cap_str_to_mln_float(s['cap']))
    return stock['symbol']

def get_sectors_with_max_and_min_stocks():
    """Return a tuple of the sectors with most and least stocks,
       discard n/a"""
    sector_cntr = Counter([s['sector'] 
      for s in data
      if s['sector'] != 'n/a'
      ])
    
    (first, *_, last) = sector_cntr.most_common()
    return (first, last)
    
    