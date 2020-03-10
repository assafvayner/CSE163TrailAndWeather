import data_getter as dg
import matplotlib.pyplot as plt
import seaborn as sns

# Hello Welcome to Zane's file.


def graph_by_hour(data):
    data = data.groupby('HOUR', as_index=False).mean()
    fig, ax = plt.subplots(1, figsize=(6, 4))
    sns.catplot(ax=ax, x='HOUR', y='Total', data=data, kind='bar')
    ax.set_title('People on the Burke Gillman Trail by Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of People')
    fig.savefig('plots/hourly.png', bbox_inches='tight')


def main():
    df = dg.get_trail_data()
    sns.set()
    graph_by_hour(df)


if __name__ == "__main__":
    main()
