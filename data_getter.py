import pandas as pd

class DataGetter:
    def get_data(self):
        trail_df = pd.read_csv('data/Burke_Gilman_Trail_north_of_NE_70th_St_Bicycle_and_Pedestrian_Counter.csv')
        trail_df = self._clean_trail_data(trail_df)
        weather_df = pd.read_csv('data/seattle-weather.csv')
        weather_df = self._clean_weather_data(weather_df)
        return trail_df, weather_df

    def _clean_weather_data(self, df):
        time = df.date.str.split('/', expand=True)
        df = df.loc[:, df.columns != 'date']
        time.columns = ['YEAR', 'MONTH', 'DAY']
        time = time.astype(int)
        df[['YEAR', 'MONTH', 'DAY']] = time
        return df

    def _clean_trail_data(self, df):
        time = df.Date.str.split(expand=True)
        time.columns = ['DATE', 'TIME', 'AM_PM']
        df['HOUR'] = self._get_time_of_day_series(time.loc[:, 'TIME':'AM_PM'])
        df[['MONTH', 'DAY', 'YEAR']] = time['DATE'].str.split("/", expand=True)
        df = df.rename(columns={'BGT North of NE 70th Total':'Total'})
        df = df.loc[:, 'Total':'YEAR']
        df = df.apply(pd.to_numeric)
        # df['DAY_OF_YEAR'] = (df['MONTH'] - 1) * 31 + df['DAY']
        return df

    def _get_time_of_day_series(self, date):
        time = date.TIME.str.split(':', expand=True)
        time = time[0].astype(int)
        # convert to 24 hour format
        time = time.where(date['AM_PM'] == 'AM', time.add(12))
        # midnight is referenced as hour being 0
        time = time.where(~((date['AM_PM'] == 'AM') & (time == 12)), 0)
        return time

    def merge_dataframes(self, trail_df, weather_df):
        return pd.merge(trail_df, weather_df,how='inner',on=['YEAR', 'MONTH', 'DAY'])