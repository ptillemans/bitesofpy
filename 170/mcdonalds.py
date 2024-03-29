import pandas as pd

data = "https://s3.us-east-2.amazonaws.com/bites-data/menu.csv"
# load the data in once, functions will use this module object
df = pd.read_csv(data)

pd.options.mode.chained_assignment = None  # ignore warnings


def get_food_most_calories(df=df):
    """Return the food "Item" string with most calories"""
    max_cal_idx = df['Calories'].idxmax()
    return df.loc[max_cal_idx]['Item']


def get_bodybuilder_friendly_foods(df=df, excl_drinks=False):
    """Calulate the Protein/Calories ratio of foods and return the
       5 foods with the best ratio.

       This function has a excl_drinks switch which, when turned on,
       should exclude 'Coffee & Tea' and 'Beverages' from this top 5.

       You will probably need to filter out foods with 0 calories to get the
       right results.

       Return a list of the top 5 foot Item stings."""
    df_cal = df[df['Calories'] > 0]
    if excl_drinks:
        drinks = df_cal[(df['Category']=='Coffee & Tea') | (df['Category']=='Beverages')].index
        df_cal.drop(drinks, inplace=True)

    df_cal['pc_ratio'] = df_cal['Protein']/df_cal['Calories']
    df_cal.sort_values(by='pc_ratio', inplace=True, ascending=False)
    top = df_cal.head(5)
    return top['Item'].tolist()