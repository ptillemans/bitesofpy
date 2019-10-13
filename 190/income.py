from pathlib import Path
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET 
from itertools import groupby

# import the countries xml file
tmp = Path('/tmp')
countries = tmp / 'countries.xml'

if not countries.exists():
    urlretrieve('https://bit.ly/2IzGKav', countries)


# namespace mapping
ns = {'wb': 'http://www.worldbank.org'}


def _get_child_text(parent :ET.Element, child_name: str) -> str:
  return parent.find(child_name, ns).text


def parse_country(country: ET.Element) -> (str, str):
  income = _get_child_text(country, 'wb:incomeLevel')
  name = _get_child_text(country, 'wb:name')
  return income, name


def get_income_distribution(xml=countries):
    """
    - Read in the countries xml as stored in countries variable.
    - Parse the XML
    - Return a dict of:
      - keys = incomes (wb:incomeLevel)
      - values = list of country names (wb:name)
    """
    root = ET.parse(xml)
    incomes = sorted([parse_country(c) for c in root.findall('wb:country', ns)])
    return {k: list(map(lambda x: x[1], g)) for k,g in groupby(incomes, key=lambda x: x[0])}

