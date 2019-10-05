from collections import namedtuple
from datetime import date

import pandas as pd

DATA_FILE = "http://projects.bobbelderbos.com/pcc/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")


def get_dataframe(fname):
   df = pd.read_csv(DATA_FILE, parse_dates=['Date'])
   return df


def prep_dataframe(df):
   df['temp'] = df['Data_Value'] / 10.0
   df.drop(columns=['Data_Value'])
   feb29s = df[(df['Date'].dt.day == 29) & (df['Date'].dt.month == 2)].index
   df.drop(feb29s, inplace=True)
   return df.drop(columns=['Data_Value'])


def extract_element(df, element):
   return df[df['Element'] == element] \
      .drop(columns=['Element']) \
      .rename(columns={'temp': element.lower()}) \
      .set_index(['ID', 'Date'])


def get_minmax_temps(df):
   df_min = extract_element(df, 'TMIN')
   df_max = extract_element(df, 'TMAX')
   return df_min.join(df_max, how='outer')

def get_historic_current(df):
   df_mm = df.reset_index(level=['ID', 'Date'])
   df_mm['doy'] = df_mm['Date'].dt.strftime("%m-%d")
   df_historic = df_mm[df_mm['Date'].dt.year < 2015] \
      .groupby(['ID', 'doy']) \
      .aggregate({'tmin': min, 'tmax': max})
   df_current = df_mm[df_mm['Date'].dt.year >= 2015] \
      .set_index(['ID', 'doy'])
   return df_historic.join(df_current, lsuffix='_h', rsuffix='_c')

def high_low_record_breakers_for_2015():
   """Extract the high and low record breaking temperatures for 2015

   The expected value will be a tuple with the highest and lowest record
   breaking temperatures for 2015 as compared to the temperature data
   provided.

   NOTE:
   The date values should not have any timestamps, should be a
   datetime.date() object. The temperatures in the dataset are in tenths
   of degrees Celsius, so you must divide them by 10

   Possible way to tackle this challenge:

   1. Create a DataFrame from the DATA_FILE dataset.

   2. Manipulate the data to extract the following:
      * Extract highest temperatures for each day / station pair between 2005-2015
      * Extract lowest temperatures for each  day / station  between 2005-2015
      * Remove February 29th from the dataset to work with only 365 days

   3. Separate data into two separate DataFrames:
      * high/low temperatures between 2005-2014
      * high/low temperatures for 2015

   4. Iterate over the 2005-2014 data and compare to the 2015 data:
      * For any temperature that is higher/lower in 2015 extract ID,
      Date, Value
      
   5. From the record breakers in 2015, extract the high/low of all the
      temperatures
      * Return those as STATION namedtuples, (high_2015, low_2015)
   """

   
   raw = get_dataframe(DATA_FILE)
   df = prep_dataframe(raw)
   df_mm = get_minmax_temps(df)
   hc = get_historic_current(df_mm)

   idx_max = hc[hc['tmax_c'] > hc['tmax_h']]['tmax_c'].idxmax()
   row_max = hc.loc[idx_max]
   station_max = STATION(idx_max[0], row_max['Date'].date(), row_max['tmax_c'])

   idx_min = hc[hc['tmin_c'] < hc['tmin_h']]['tmin_c'].idxmin()
   row_min = hc.loc[idx_min]
   station_min = STATION(idx_min[0], row_min['Date'].date(), row_min['tmin_c'])

   return station_max, station_min

     