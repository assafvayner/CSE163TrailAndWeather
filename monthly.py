from data_getter import DataGetter
import seaborn as sns
import matplotlib.pyplot as plt


def graph_months(df):
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
        # ax = axs[(month + 12) // 4][(month + 12) % 4]
        # graph_titles(ax, month)
    fig.savefig('plots/monthly.png')


def graph_titles(ax, month):
    ax.set_title(month_name(month, False))
    ax.set_xlabel('Day of the Month')
    ax.set_ylabel('Total Bikers and Pedestrians both directions')
    # ax.set(ylim=(0, 500))


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
        user_month = df[df['MONTH'] == month_index]
        user_month_grouped = user_month.groupby('DAY', as_index=False).mean()
        day = res[month_index]['DAY']
        user_day = user_month[user_month['DAY'] == day]
        user_day_grouped = user_day.groupby('HOUR', as_index=False).mean()
        fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        sns.barplot(ax=ax2, x='HOUR', y='Total', data=user_day_grouped)
        sns.barplot(ax=ax1, x='DAY', y='Total', data=user_month_grouped)
        fig.savefig('plots/' + month.lower() + '.png')
        fancy_hour_printer(res, month_index)


def fancy_hour_printer(res, month_index):
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


def month_to_index(month, Jan_is_One=False):
    month = month.lower()
    months = ('january', 'febuary', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december')
    if month not in months:
        return None
    return months.index(month) + Jan_is_One


def main():
    dg = DataGetter()
    trail_data = dg.get_trail_data()
    sns.set()
    lowest_per_month(trail_data, 'January')
    # lowest_per_month(trail_data)


if __name__ == '__main__':
    main()
