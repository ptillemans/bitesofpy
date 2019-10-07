from os import path, environ
from urllib.request import urlretrieve

import pandas as pd

EXCEL = path.join(environ.get('TEMP', '/tmp'), 'order_data.xlsx')
if not path.isfile(EXCEL):
    urlretrieve('https://bit.ly/2JpniQ2', EXCEL)


def load_excel_into_dataframe(excel=EXCEL):
    """Load the SalesOrders sheet of the excel book (EXCEL variable)
       into a Pandas DataFrame and return it to the caller"""
    return pd.read_excel(EXCEL, 'SalesOrders')


def get_year_region_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Group the DataFrame by year and region, summing the Total
       column. You probably need to make an extra column for
       year, return the new df as shown in the Bite description"""
    df['Year'] = df['OrderDate'].dt.year
    return df.pivot_table(index=['Year', 'Region'], aggfunc=sum)['Total']


def get_most_of_by(df, thing, crit):
    """Return the name of the thing which has sold the 
    most by some criterium"""
    most = df.groupby(thing).sum().nlargest(1,[crit])
    name = most.index[0]
    total = most[crit][0]
    return name,total

def get_best_sales_rep(df: pd.DataFrame):
    """Return a tuple of the name of the sales rep and
       the total of his/her sales"""
    return get_most_of_by(df, 'Rep', 'Total')


def get_most_sold_item(df):
    """Return a tuple of the name of the most sold item
       and the number of units sold"""
    return get_most_of_by(df, 'Item', 'Units')
