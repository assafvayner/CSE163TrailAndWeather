import pandas as pd
import numpy as np

class DataGetter:
    def get_data(self, day_of_week=True):
        return self.get_trail_data(day_of_week), self.get_weather_data(day_of_week)


    def get_trail_data(self, day_of_week=True):
        trail_df = pd.read_csv('data/Burke_Gilman_Trail_north_of_NE_70th_St_Bicycle_and_Pedestrian_Counter.csv')
        trail_df = self._clean_trail_data(trail_df, day_of_week)
        return trail_df
    

    def get_weather_data(self, day_of_week=True):
        weather_df = pd.read_csv('data/seattle-weather.csv')
        weather_df = self._clean_weather_data(weather_df, day_of_week)
        return weather_df


    def _clean_weather_data(self, df, day_of_week):
        time = df.date.str.split('/', expand=True)
        df = df.loc[:, df.columns != 'date']
        time.columns = ['YEAR', 'MONTH', 'DAY']
        time = time.astype(int)
        df[['YEAR', 'MONTH', 'DAY']] = time
        self._add_day_of_week(df, day_of_week)
        return df


    def _clean_trail_data(self, df, day_of_week):
        time = df.Date.str.split(expand=True)
        time.columns = ['DATE', 'TIME', 'AM_PM']
        df['HOUR'] = self._get_time_of_day_series(time.loc[:, 'TIME':'AM_PM'])
        df[['MONTH', 'DAY', 'YEAR']] = time['DATE'].str.split("/", expand=True)
        df = df.rename(columns={'BGT North of NE 70th Total':'Total'})
        df = df.loc[:, 'Total':'YEAR']
        df = df.apply(pd.to_numeric)
        df = self._add_day_of_week(df, day_of_week)
        return df

    def _add_day_of_week(self, df, day_of_week):
        if day_of_week:
            df['DAY_OF_WEEK'] = np.vectorize(self._day_of_week)(df['DAY'], df['MONTH'], df['YEAR']).astype(int)
        return df


    def _get_time_of_day_series(self, date):
        time = date.TIME.str.split(':', expand=True)
        time = time[0].astype(int)
        # convert to 24 hour format
        time = time.where((date['AM_PM'] == 'AM') | (time == 12), time.add(12))
        # midnight is referenced as hour being 24
        time = time.where(~((date['AM_PM'] == 'AM') & (time == 12)), 24)
        return time


    def _day_of_week(self, d, m, y):
        """
        returns day of the week given the input d(ay), m(onth), y(ear)
        year expected in 21st century, 1 <= m <= 12
        returns day of week where 0 = Sunday, 1 = Monday...
        """
        t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
        y -= m < 3
        return round(y + y/4 - y/100 + y/400 + t[m-1] + d) % 7

    def merge_dataframes(self, trail_df, weather_df):
        merge_terms = ['YEAR', 'MONTH', 'DAY']
        if 'DAY_OF_WEEK' in trail_df.columns and 'DAY_OF_WEEK' in weather_df.columns:
            merge_terms.append('DAY_OF_WEEK')
        return pd.merge(trail_df, weather_df,how='inner',on=merge_terms)
