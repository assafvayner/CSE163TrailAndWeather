import data_getter as dg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def commute_pattern(df):
    """
    It should take the file and filter it so it can be seperated by days and hours.
    in the morning, if bike south is more than bike north, it should return 1;
    in the evening, if bike north is more than bike south, it should return 1;
    if in a day, both morning and evening returns 1, the day should return 1,
    else, return 0.
    It should end up calculating the percentage of days that returns 1
    """
    # is_0 = df['DAY_OF_WEEK'] == 0
    # is_6 = df['DAY_OF_WEEK'] == 6
    # morning_data = df[(df['HOUR']>= 7) & (df['HOUR']<= 10)]
    # morning_data = morning_data[is_0| is_6]
    # evening_data = df[(df['HOUR']>= 16) & (df['HOUR']<= 19)]
    # evening_data = evening_data[is_0| is_6]
    morning_data = df[(df['HOUR']>= 7) & (df['HOUR']<= 10)& (df['DAY_OF_WEEK']>0)& (df['DAY_OF_WEEK']<6)]
    evening_data = df[(df['HOUR']>= 16) & (df['HOUR']<= 19) & (df['DAY_OF_WEEK']>0)& (df['DAY_OF_WEEK']<6)]
    morning_indiv= morning_data.groupby(['YEAR','MONTH','DAY'])
    evening_indiv = evening_data.groupby(['YEAR','MONTH','DAY'])
    morning_diff = morning_indiv['Bike South'].sum() - morning_indiv['Bike North'].sum()
    evening_diff = evening_indiv['Bike North'].sum()- evening_indiv['Bike South'].sum()
    morning_list = []
    sm_morning_list = []
    for i in morning_diff:
        sm_morning_list.append(i)
        if i > 0:
            morning_list.append(1)
        else:
            morning_list.append(0)
    morning_list = pd.Series(morning_list,name = 'Pattern')
    sm_morning_list = pd.Series(sm_morning_list, name = 'Morning Diff')
    evening_list = []
    sm_evening_list = []
    for i in evening_diff:
        sm_evening_list.append(i)
        if i > 0:
            evening_list.append(1)
        else:
            evening_list.append(0)
    evening_list = pd.Series(evening_list,name = 'Pattern')
    sm_evening_list = pd.Series(sm_evening_list, name = 'Evening Diff')
    count = 0
    for i in range(len(morning_list)):
        if morning_list[i] == 1:
            if morning_list[i] == evening_list[i]:
                count+=1
    return count/len(morning_list)


def plot_pattern(df):
    """
    plot the graph with x-axis of commuting hours
    and y-axis of the number of difference of people
    biking south and biking north.
    """
    days_of_week = (df['DAY_OF_WEEK'] > 0) & (df['DAY_OF_WEEK'] < 6)
    morning_data = (df['HOUR']>= 7) & (df['HOUR']<= 10)
    evening_data = (df['HOUR']>= 16) & (df['HOUR']<= 19)
    df = df[(morning_data | evening_data) & days_of_week]
    df['diff'] = df.loc[:, 'Bike South'] - df.loc[:, 'Bike North']
    filtered_df = df.groupby(['HOUR'], as_index=False).mean()
    sns.catplot(x='HOUR', y='diff', data = filtered_df, kind='bar')
    plt.title("Pattern of commuting days")
    plt.xlabel('Hour')
    plt.ylabel('Difference bettwen bike south and bike north')
    plt.savefig('plots/commuter_pattern.png',bbox_inches='tight')

def main():
    df = dg.get_trail_data()
    print(commute_pattern(df))
    plot_pattern(df)


if __name__ == "__main__":
    main()