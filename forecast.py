from data_getter import DataGetter
import utils
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

def weather_predictor(df):
    df = df.dropna()
    X = df.loc[:, 'Total':'DAY_OF_WEEK']#(df.columns != 'weather')] #
    y = df['weather']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    print('weather_predictor')
    print(f'training set error rate: {100*utils.error_rate(y_train.to_numpy(dtype=str), y_pred_train)}%')
    print(f'test set error rate: {100*utils.error_rate(y_test.to_numpy(dtype=str), y_pred_test)}%')


def main():
    data_getter = DataGetter()
    trail_df, weather_df = data_getter.get_data()
    merged = data_getter.merge_dataframes(trail_df, weather_df)
    utils.print_heads(trail_df, weather_df, merged)
    print(merged.columns)
    weather_predictor(merged)
    

if __name__ == '__main__':
    main()