import data_getter as dg
import matplotlib.pyplot as plt
import seaborn as sns

# These functions allow the user to plot the average number of people for each
# hour of the day.


def graph_by_hour(data):
    """
    Computes the average values for every hour, then plots the data in a bar
    plot
    """
    data = data.groupby('HOUR', as_index=False).mean()
    fig, ax = plt.subplots(1, figsize=(6, 4))
    sns.barplot(ax=ax, x='HOUR', y='Total', data=data)
    ax.set_title('People on the Burke Gillman Trail by Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of People')
    fig.savefig('plots/hourly.png', bbox_inches='tight')


def main():
    """
    Imports the data, sets up seaborn, and runs the graphing function
    """
    df = dg.get_trail_data()
    sns.set()
    graph_by_hour(df)


if __name__ == "__main__":
    main()
