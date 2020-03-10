from data_getter import DataGetter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
Command:
git add "file_name"
git commit -m "What you changed"
git push

"""


def commute_pattern(df):
    is_0 = df['DAY_OF_WEEK'] == 0
    is_6 = df['DAY_OF_WEEK'] == 6
    morning_data = df[(df['HOUR']>= 7) & (df['HOUR']<= 10)& (df['DAY_OF_WEEK']>0)& (df['DAY_OF_WEEK']<6)]
    #morning_data = morning_data[is_0| is_6]
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
    #new_morning_diff = pd.concat([sm_morning_list,morning_list],axis = 1)

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
    #new_evening_diff = pd.concat([sm_evening_list,evening_list],axis = 1)
    count = 0
    for i in range(len(morning_list)):
        if morning_list[i] == 1:
            if morning_list[i] == evening_list[i]:
                count+=1
    return count/len(morning_list)
    #count/len(morning_list)
    #& (df['DAY_OF_WEEK']>0)& (df['DAY_OF_WEEK']<6)


def plot_pattern(df):
    filtered_df = df.groupby(['DAY_OF_WEEK','HOUR'])
    value = filtered_df['Bike South'].sum()-filtered_df['Bike North'].sum()
    # value = pd.DataFrame(value[0]).reset_index()
    # value.columns = ['Hour', 'Mean']
    # sns.relplot(x='Hour', y='Mean', data=value, kind='line')
    # plt.savefig('test.png', bbox_inches='tight')
    return value
def main():
    dg = DataGetter()
    df = dg.get_trail_data()
    print(commute_pattern(df))
    print(plot_pattern(df).to_string())


if __name__ == "__main__":
    main()