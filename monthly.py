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
        graph_titles(ax, month)
        sns.barplot(x='DAY', y='Total', data=data, ax=ax)
        ax = axs[(month + 12) // 4][(month + 12) % 4]
        graph_titles(ax, month)
        sns.lineplot(x='DAY', y='Total', data=data, ax=ax)
    fig.savefig('plots/monthly.png')


def graph_titles(ax, month):
    ax.set_title(month_name(month, False))
    ax.set_xlabel('Day of the Month')
    ax.set_ylabel('Total Bikers and Pedestrians both directions')


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
        grouped_by_month = df.groupby('MONTH')
        # gb = dict(list(gb))
        for k, gb in grouped_by_month:
            a = gb.groupby(['HOUR', 'DAY'], as_index=False).mean()
            res[k] = a['Total'].idxmin()
        print(res)
            

def main():
    dg = DataGetter()
    trail_data = dg.get_trail_data()
    # graph_months(trail_data)
    lowest_per_month(trail_data)


if __name__ == '__main__':
    main()