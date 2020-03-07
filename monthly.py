from data_getter import DataGetter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def graph_months(df):
    sns.set()
    fig, axs = plt.subplots(6, 4, figsize=(40, 60))
    gb = df.groupby('MONTH')
    gb = dict(list(gb))
    for month in range(12):
        month_df = gb[month + 1]
        ax = axs[month // 4][month % 4]
        data = month_df.groupby('DAY', as_index=False)[month_df.columns[:5]].mean()
        # data.plot(x='DAY', y='Total', ax=ax, kind='line')
        ax.set_title(month_name(month, False))
        sns.barplot(x='DAY', y='Total', data=data, ax=ax)#, size=100)
        ax = axs[(month + 12) // 4][(month + 12) % 4]
        ax.set_title(month_name(month, False))
        ax.xlabel()
        sns.lineplot(x='DAY', y='Total', data=data, ax=ax)
    fig.savefig('plots/monthly.png')


def month_name(n, Jan_is_One=True):
    """
    returns the string for the month given the number, assumes January is month
    number 1 however if Jan_is_zero is true, January is month number 0 and all
    other months are likewise decremented.
    """
    if(n - Jan_is_One >= 12 or n - Jan_is_One < 0):
        return None
    return ('January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November',
            'December')[n - Jan_is_One]

def lowest_per_month(df, month=None):
    if month is None:
        res = dict()
        gb = df.groupby('MONTH')
        gb = dict(list(gb))
        for m in range(12):
            month_df = gb[m + 1]
            v = month_df['Total'].min()
            print(v)

def main():
    dg = DataGetter()
    trail_data = dg.get_trail_data()
    # graph_months(trail_data)
    lowest_per_month(trail_data)


if __name__ == '__main__':
    main()