import pandas as pd
import numpy as np


def get_data(day_of_week=True):
    """
    returns both dataframes for the trail data first and then the weather data
    """
    trail_df = get_trail_data(day_of_week)
    weather_df = get_weather_data(day_of_week)
    return trail_df, weather_df


def get_trail_data(day_of_week=True):
    """
    returns the cleaned trail data
    """
    trail_df = pd.read_csv('data/Burke_Gilman_Trail_north_of_NE_70th_St_' +
                           'Bicycle_and_Pedestrian_Counter.csv')
    trail_df = _clean_trail_data(trail_df, day_of_week)
    trail_df = _remove_in_trail_data(trail_df)
    return trail_df


def _remove_in_trail_data(df):
    """
    removes missing data from the trail dataset
    """
    df = _remove(df, 2018, [6, 7, 8])
    df = _remove(df, 2018, 5, [30, 31])
    df = _remove(df, 2018, 9, range(1, 7))
    return df


def _remove(df, years, months=range(1, 13), days=range(1, 32)):
    """
    removes data from the given ranges or values
    """
    if isinstance(days, int):
        days = [days]
    if isinstance(months, int):
        months = [months]
    if isinstance(years, int):
        years = [years]
    for day in days:
        for month in months:
            for year in years:
                # print(f'day: {day}, month: {month}, year: {year}')
                df = df[~((df['DAY'] == day) & (df['MONTH'] == month) &
                          (df['YEAR'] == year))]
    return df


def get_weather_data(day_of_week=True):
    """
    returns the cleaned weather data
    """
    weather_df = pd.read_csv('data/seattle-weather.csv')
    weather_df = _clean_weather_data(weather_df, day_of_week)
    return weather_df


def _clean_weather_data(df, day_of_week):
    """
    takes uncleaned weather data, and returns it cleaned
    """
    time = df.date.str.split('/', expand=True)
    df = df.loc[:, df.columns != 'date']
    time.columns = ['YEAR', 'MONTH', 'DAY']
    time = time.astype(int)
    df[['YEAR', 'MONTH', 'DAY']] = time
    _add_day_of_week(df, day_of_week)
    return df


def _clean_trail_data(df, day_of_week):
    """
    takes in uncleaned trail data and returns cleaned data
    """
    time = df.Date.str.split(expand=True)
    time.columns = ['DATE', 'TIME', 'AM_PM']
    df['HOUR'] = _get_time_of_day_series(time.loc[:, 'TIME':'AM_PM'])
    df[['MONTH', 'DAY', 'YEAR']] = time['DATE'].str.split("/", expand=True)
    df = df.rename(columns={'BGT North of NE 70th Total': 'Total'})
    df = df.loc[:, 'Total':'YEAR']
    df = df.apply(pd.to_numeric)
    df = _add_day_of_week(df, day_of_week)
    return df


def _add_day_of_week(df, day_of_week):
    """
    adds the day of week column to the dataframe if day_of_week is True
    """
    if day_of_week:
        d_o_w = np.vectorize(_day_of_week)
        temp_ser = d_o_w(df['DAY'], df['MONTH'], df['YEAR']).astype(int)
        df['DAY_OF_WEEK'] = temp_ser
    return df


def _get_time_of_day_series(date):
    """
    adds the time of day column to the trail dataframe
    """
    time = date.TIME.str.split(':', expand=True)
    time = time[0].astype(int)
    # convert to 24 hour format
    time = time.where((date['AM_PM'] == 'AM') | (time == 12), time.add(12))
    # midnight is referenced as hour being 24
    time = time.where(~((date['AM_PM'] == 'AM') & (time == 12)), 24)
    return time


def _day_of_week(d, m, y):
    """
    returns day of the week given the input d(ay), m(onth), y(ear)
    year expected in 21st century, 1 <= m <= 12
    returns day of week where 0 = Sunday, 1 = Monday...
    """
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    return round(y + y/4 - y/100 + y/400 + t[m-1] + d) % 7


def merge_dataframes(trail_df, weather_df):
    """
    takes the trail and weather dataframes and returns the merged dataframe
    """
    merge_terms = ['YEAR', 'MONTH', 'DAY']
    if 'DAY_OF_WEEK' in trail_df.columns and 'DAY_OF_WEEK' in \
            weather_df.columns:
        merge_terms.append('DAY_OF_WEEK')
    return pd.merge(trail_df, weather_df, how='inner', on=merge_terms)
