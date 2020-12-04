''' process weather data '''

import pandas as pd
import numpy as np

BASE_PATH = "./data/rawdatasets/weather_data/"
LIMIT = "./lists/working_sites_updated_v2.csv"
SAVE_PATH = "./data/"
ISD_FORM = {0:'year', 1:'month', 2:'day', 3:'hour', 4:'air_temp', 5:'dew_point', 6:'pressure (kpa)', 7:'wind direction',
    8:'wind speed', 9:'sky condition total coverage code', 10:'precipitation depth 1 hr', 11:'precipitation depth 6 hr'}


def pol2cart(parameters):
    # polar to cartesian
    r, theta = parameters
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return (x, y)


# extract all weather data
def get_wind_data(station, year):
    # the input is a station name
    working_sites = pd.read_csv(LIMIT)
    id_lists = working_sites[working_sites['city']==station]['station_id']
    # check whether city is unique or empty
    assert len(id_lists)==1, 'Either duplicates or not the the working sites list'

    for each in id_lists:
        print(each)
        df = pd.read_fwf(f'./data/rawdatasets/weather_data/china_isd_lite_{year}/{each}-99999-{year}', header=None)

    df = df.rename(columns=ISD_FORM)

    # create timestamp
    df['time'] = pd.to_datetime(df[['year', 'month', 'day']])
    df['time'] += pd.to_timedelta(df.hour, unit='h')

    df.drop(columns= ['year', 'month', 'day', 'hour'], inplace=True)

    df = df.set_index('time')

    # fill in the missing data
    df = df.replace({-9999.: np.nan})

    idx = pd.date_range(pd.to_datetime(f'{year}-01-01 00:00:00'),\
         pd.to_datetime(f'{year}-12-31 23:00:00'), freq='h')
    df = df.reindex(idx, fill_value=np.nan)

    df['wind direction'].interpolate(method='time', inplace=True)
    df['wind speed'].interpolate(method='time', inplace=True)

    # rescale
    for feature in ['air_temp', 'dew_point', 'wind speed']:
        df[feature] = df[feature] / 10

    df['pressure (kpa)'] = df['pressure (kpa)'] / 100

    # calculate the wind vectors
    df['wind_vector'] = df[['wind speed', 'wind direction']].apply(pol2cart, axis=1)

    return df


