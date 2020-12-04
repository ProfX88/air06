''' impute nan data using TimeSeries interpolation'''

import pandas as pd
import numpy as np


def time_interpolation_impute(df):
    cities = df.columns.unique()
    for city in cities:
        if city !='index' and city != 'date' and city != 'hour' and city != 'type':
            if df[city].isnull().sum() > 0:
                df[city].interpolate(method='time', inplace=True)

    return df




