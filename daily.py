from data_getter import DataGetter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Hello Welcome to Zane's file.


def graph_by_hour(data):
    # data = data[data['Total'] < 1000]
    data = data.groupby('HOUR', as_index=False).mean()
    # data = data.loc[:23]
    # test_data = data.loc[:, ['Total', 'HOUR']]
    # data = data['Total']
    fig, ax = plt.subplots(1, figsize=(10, 5))
    sns.catplot(ax=ax, x='HOUR', y='Total', data=data, kind='bar')
    ax.set_title('People on the Burke Gillman Trail by Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of People')
    # data = data['Total']

    # data.plot(kind='bar')
    # data = data[data['HOUR'] == 12]
    # print(data)
    fig.savefig('plots/test.png')


def main():
    dg = DataGetter()
    df = dg.get_trail_data()
    sns.set()
    graph_by_hour(df)


if __name__ == "__main__":
    main()
