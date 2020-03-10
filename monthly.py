from data_getter import DataGetter
import seaborn as sns
import matplotlib.pyplot as plt

# These functions allow the user to get the hour with the lowest average number
# of people. If a month is specified, it graphs the month with daily averages
# and a graph of the day with the lowest hour, hour by hour. If a month is not
# specified, it graphs all days of the year seperated by month.


def graph_months(df):
    """
    Graphs every days' average number of trail users divided by month
    """
    fig, axs = plt.subplots(3, 4, figsize=(40, 25))
    gb = df.groupby('MONTH')
    gb = dict(list(gb))
    for month in range(12):
        month_df = gb[month + 1]
        ax = axs[month // 4][month % 4]
        data = month_df.groupby('DAY',
                                as_index=False)[month_df.columns[:5]].mean()
        graph_titles(ax, month)
        sns.barplot(x='DAY', y='Total', data=data, ax=ax)
    fig.savefig('plots/monthly.png')


def graph_day(df, month, month_index, res):
    """
    Graphs the specified month (day by day) as well as the specified hour
    (hour by hour). Also takes as a parameter month_index (month number
    starting at 0) and res (a dictionary of dictionaries storing the least
    busy days and weeks)
    """
    user_month = df[df['MONTH'] == month_index]
    user_month_grouped = user_month.groupby('DAY', as_index=False).mean()
    day = res[month_index]['DAY']
    user_day = user_month[user_month['DAY'] == day]
    user_day_grouped = user_day.groupby('HOUR', as_index=False).mean()
    fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
    sns.barplot(ax=ax2, x='HOUR', y='Total', data=user_day_grouped)
    graph_titles(ax2, None, True)
    sns.barplot(ax=ax1, x='DAY', y='Total', data=user_month_grouped)
    graph_titles(ax1, month_index - 1)
    fig.savefig('plots/' + month.lower() + '.png')


def graph_titles(ax, month, day=False):
    """
    Sets the titles for the graphs. If day is False (default), it titles the
    the graph for month (day by day). If day is True, it titles the graph for
    day (hour by hour)
    """
    ax.set_ylabel('Total Bikers and Pedestrians in both Directions')
    if day:
        ax.set_title('Hour of the Month with the Lowest Number of People')
        ax.set_xlabel('Hours of the Day')
        ax.set_ylabel('Total Bikers and Pedestrians both directions')
    else:
        ax.set_title(month_name(month, False))
        ax.set_xlabel('Day of the Month')


def month_name(n, Jan_is_One=True):
    """
    Returns the string for the month given the number, assumes January is month
    number 1. If Jan_is_zero is true, January is month number 0 and all other
    months are likewise decremented
    """
    if(n - Jan_is_One >= 12 or n - Jan_is_One < 0):
        return None
    return ('January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November',
            'December')[n - Jan_is_One]


def lowest(df, month=None):
    """
    Calculates the lowest hour for every month of the year. If no month is
    specified, graphs all 365 days and prints the lowest hour of each month.
    If month is specified, graphs that month (day by day) and the day with
    the lowest hour (hour by hour) and outputs the lowest hour for that month
    """
    res = dict()
    grouped_by_month = df.groupby('MONTH')
    for k, gb in grouped_by_month:
        by_day_and_hour = gb.groupby(['HOUR', 'DAY'], as_index=False).mean()
        min_idx = by_day_and_hour['Total'].idxmin()
        res[k] = {'DAY': by_day_and_hour.loc[min_idx, 'DAY'],
                  'HOUR': by_day_and_hour.loc[min_idx, 'HOUR']}
    if month is None:
        graph_months(df)
        for n in range(12):
            fancy_hour_printer(res, n + 1)
    else:
        month_index = month_to_index(month, True)
        graph_day(df, month, month_index, res)
        fancy_hour_printer(res, month_index)


def fancy_hour_printer(res, month_index):
    """
    Prints the hour with the lowest number of people given the specified
    month (month_index). Takes in dictionary of dictionaries (res) storing
    the lowest day and hour of each month
    """
    day = res[month_index]['DAY']
    hour = res[month_index]['HOUR']
    month = month_name(month_index)
    if hour == 24:
        time = (str)(hour - 12) + ':00 AM'
    elif hour >= 11:
        time = (str)(hour - 12) + ':00 PM'
    else:
        time = (str)(hour) + ':00 AM'
    print('Hour in ' + month + ' with the lowest number of people: ' +
          (str)(month_index) + '/' + (str)(day) + ' at ' + time)


def month_to_index(month, Jan_is_one=False):
    """
    Returns an int signifying the number of the given month. If Jan_is_one is
    False (default), returns the index value starting at 0 (January = 0). If
    Jan_is_one is True, returns the index starting at 1 (January = 1)
    """
    month = month.lower()
    months = ('january', 'febuary', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december')
    if month not in months:
        return None
    return months.index(month) + Jan_is_one


def main():
    """
    Imports data, sets up seaborn, and calls the lowest function
    """
    dg = DataGetter()
    trail_data = dg.get_trail_data()
    sns.set()
    lowest(trail_data, 'October')
    lowest(trail_data)


if __name__ == '__main__':
    main()
