'''deal with the rawdatasets'''

import pandas as pd
import numpy as np
import glob
import os
import sys

BASE_PATH = "data/rawdatasets/city_AQI"
LIMIT = "data/rawdatasets/working_sites_data.csv"

def get_a_year_data(query):
    the_year_dir = os.path.join(BASE_PATH, f'city_{query}')
    all_files = os.listdir(the_year_dir)
    li=[]
    for filename in all_files:
        df = pd.read_csv(os.path.join(the_year_dir,filename), index_col=None, header=0)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df = df.sort_values(by='date')

    return df


def extract_type_data(df, query):
    # for example: query = 'PM2.5_24h', extract only 24hr average pm2.5 data
    return df[df['type'].isin(query)]


def limit_stations(df):
    working_site = pd.read_csv(LIMIT, index_col=None)
    selected = pd.concat([df[['date', 'hour', 'type']], df[working_site['station name']]], axis=1)

    d={}
    i = 0
    for name in working_site['station name']:
        d.update({working_site['station name'][i]: working_site['city'][i]})
        i += 1

    # remove duplicate english names for cities
    d['伊春'] = 'Yeechun'

    selected = selected.rename(columns = d)
    # Drop duplicated columns e.g. Chaoyang
    selected = selected.loc[:, ~selected.columns.duplicated()]

    # Turn time into datetime
    selected['timestamp'] = pd.to_datetime(selected.date, format='%Y%m%d')
    selected['timestamp'] += pd.to_timedelta(selected.hour, unit='h')
    selected.set_index('timestamp', inplace = True)
    selected.sort_values(by='timestamp', inplace = True)

    return selected


def get_data_timesector(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return df.loc[start_date : end_date]

def fill_missing_time(df):
    idx = pd.date_range(min(df.index), max(df.index), freq='h')
    return df.reindex(idx, fill_value=np.nan)



def main():
    start = input("start time? (in the format as 20190101-00) \n> ")
    end = input("end time? in the format as 20191231-23) \n> ")
    start_time = pd.to_datetime(start)
    end_time = pd.to_datetime(end)
    start_year = start_time.year
    end_year = end_time.year

    if start_year == end_year:
        data = get_a_year_data(start_year)
    elif start_year < end_year:
        data = get_a_year_data(start_year)
        for yr in range(start_year+1, end_year+1):
            data = data.append(get_a_year_data(yr))
    else:
        print('Wrong date!!!')

    query = input("Pollutant type?\n> ")
    if bool(query):
        default_list = [query]
        data = extract_type_data(data, default_list)

    data = limit_stations(data)

    data = get_data_timesector(data, start, end)

    data = fill_missing_time(data)

    print(data)
    return data


if __name__ == '__main__':
    data = main()
