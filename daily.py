from data_getter import DataGetter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Hello Welcome to Zane's file.


def graph_by_hour(data):
    #data = data[data['Total'] < 1000]
    #data = data.groupby('HOUR').mean()
    data = data.loc[:23]
    # test_data = data.loc[:, ['Total', 'HOUR']]
    # data = data['Total']
    # sns.catplot(x='HOUR', y='Total', data=test_data, kind='bar')
    data = data['Total']
    
    data.plot(kind='bar')
    plt.savefig('test.png')
    # print(test_data)


def main():
    dg = DataGetter()
    df = dg.get_trail_data()
    sns.set()
    # print(df)
    graph_by_hour(df)


if __name__ == "__main__":
    main()
