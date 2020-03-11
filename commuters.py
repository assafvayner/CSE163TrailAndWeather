import data_getter as dg
import matplotlib.pyplot as plt
import seaborn as sns

# morning is defined as 7 am to 10 am inclusive
# evening is defined as 4 pm to 7 pm inclusive


def commute_pattern(morning_data, evening_data):
    """
    It should take the dataframe and filter so it can be
    seperated by days and hours.
    in the morning, if bike south is more than bike north, it should return 1;
    in the evening, if bike north is more than bike south, it should return 1;
    if in a day, both morning and evening returns 1, the day should return 1,
    else, return 0.
    It should end up calculating the percentage of days that returns 1
    """
    morning_indiv = morning_data.groupby(['YEAR', 'MONTH', 'DAY'])
    evening_indiv = evening_data.groupby(['YEAR', 'MONTH', 'DAY'])
    morning_diff = morning_indiv['Bike South'
                                 ].sum() - morning_indiv['Bike North'].sum()
    evening_diff = evening_indiv['Bike North'
                                 ].sum() - evening_indiv['Bike South'].sum()
    m_list = [1 if i > 0 else 0 for i in morning_diff.tolist()]
    e_list = [1 if i > 0 else 0 for i in evening_diff.tolist()]
    count = sum([1 for m, e in zip(m_list, e_list) if m == e and m == 1])
    return count / len(m_list)


def filter_weekend(df):
    """
    filters data for weekend days and the hours defined as morning and evening
    and returns the morning and evening data in separate dataframes
    """
    is_0 = df['DAY_OF_WEEK'] == 0
    is_6 = df['DAY_OF_WEEK'] == 6
    morning_data = df[(df['HOUR'] >= 7) & (df['HOUR'] <= 10) & (is_0 | is_6)]
    evening_data = df[(df['HOUR'] >= 16) & (df['HOUR'] <= 19) & (is_0 | is_6)]
    return morning_data, evening_data


def filter_weekday(df):
    """
    filters data for weekdays and the hours defined as morning and evening
    and returns the morning and evening data in separate dataframes
    """
    morning_data = df[(df['HOUR'] >= 7) & (df['HOUR'] <= 10) &
                      (df['DAY_OF_WEEK'] > 0) & (df['DAY_OF_WEEK'] < 6)]
    evening_data = df[(df['HOUR'] >= 16) & (df['HOUR'] <= 19)
                      & (df['DAY_OF_WEEK'] > 0) & (df['DAY_OF_WEEK'] < 6)]
    return morning_data, evening_data


def plot_pattern(df):
    """
    plot the graph with x-axis of commuting hours
    and y-axis of the number of difference of people
    biking south and biking north.
    """
    days_of_week = (df['DAY_OF_WEEK'] > 0) & (df['DAY_OF_WEEK'] < 6)
    morning_data = (df['HOUR'] >= 7) & (df['HOUR'] <= 10)
    evening_data = (df['HOUR'] >= 16) & (df['HOUR'] <= 19)
    df = df[(morning_data | evening_data) & days_of_week]
    # following line produces warning, need not worry about it
    # suggested fixes produce worse warnings
    df['diff'] = df.loc[:, 'Bike South'] - df.loc[:, 'Bike North']
    filtered_df = df.groupby(['HOUR'], as_index=False).mean()
    sns.catplot(x='HOUR', y='diff', data=filtered_df, kind='bar')
    plt.title("Pattern of commuting days")
    plt.xlabel('Hour')
    plt.ylabel('Difference bettwen bike south and bike north')
    plt.savefig('plots/commuter_pattern.png', bbox_inches='tight')


def main():
    df = dg.get_trail_data()
    print('percent of weekdays exhibiting commuting pattern: ', end='')
    weekday_m, weekday_e = filter_weekday(df)
    print(str(100 * commute_pattern(weekday_m, weekday_e)) + '%')
    print('percent of weekend days exhibiting commuting pattern: ', end='')
    weekend_m, weekend_e = filter_weekend(df)
    print(str(100 * commute_pattern(weekend_m, weekend_e)) + '%')
    plot_pattern(df)


if __name__ == "__main__":
    main()
