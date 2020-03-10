import numpy as np


def error_rate(true_vals, predictions):
    bool_arr = true_vals[:] == predictions[:]
    return np.count_nonzero(~bool_arr) / len(bool_arr)


def hasNaN(df):
    return len(df) != len(df.dropna())


def print_heads(trail_df=None, weather_df=None, merged=None):
    if trail_df is not None:
        print('trail_df')
        print(trail_df.head())
        print()
    if weather_df is not None:
        print('weather_df')
        print(weather_df.head())
        print()
    if merged is not None:
        print('merged')
        print(merged.head())
        print()
