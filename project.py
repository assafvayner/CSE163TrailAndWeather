from data_getter import DataGetter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.neural_network import MLPClassifier, MLPRegressor

def weather_predictor(df):
    df = df.dropna()
    X = df.loc[:, 'Total':'YEAR']#(df.columns != 'weather')] #
    y = df['weather']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    print('weather_predictor')
    print(f'training set error rate: {100*error_rate(y_train.to_numpy(dtype=str), y_pred_train)}%')
    print(f'test set error rate: {100*error_rate(y_test.to_numpy(dtype=str), y_pred_test)}%')

def pseudo_clock(df):
    df = df.dropna()
    X = df.loc[:, 'Total':'DAY']
    X = X.loc[:, X.columns != 'HOUR']
    y = df['HOUR']
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    print('peudo_clock')
    print(f'training set MSE: {mean_squared_error(y_train, y_pred_train)}')
    print(f'test set MSE: {mean_squared_error(y_test, y_pred_test)}')


def pseudo_clock_NN(df):
    df = df.dropna()
    X = df.loc[:, 'Total':'DAY']
    X = X.loc[:, X.columns != 'HOUR']
    y = df['HOUR']
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    min_n = 5
    min_error_sum = 200
    for num_hidden in range(5,100):
        model = MLPRegressor(num_hidden)
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        print('peudo_clock_NN with num_hidden: ' + str(num_hidden))
        error_train = mean_squared_error(y_train, y_pred_train)
        print(f'training set MSE: {error_train}')
        error_test = mean_squared_error(y_test, y_pred_test)
        print(f'test set MSE: {error_test}')
        if min_error_sum > error_test + error_train:
            min_n = num_hidden
    print(f'minimum hidden layers: {min_n}')



def error_rate(true_vals, predictions):
    bool_arr = true_vals[:] == predictions[:]
    return np.count_nonzero(~bool_arr) / len(bool_arr)


def hasNaN(df):
    return len(df) != len(df.dropna())


def print_heads(trail_df, weather_df, merged):
    print('trail_df')
    print(trail_df.head())
    print()
    print('weather_df')
    print(weather_df.head())
    print()
    print('merged')
    print(merged.head())

def main():
    data_getter = DataGetter()
    trail_df, weather_df = data_getter.get_data()
    merged = data_getter.merge_dataframes(trail_df, weather_df)
    print_heads(trail_df, weather_df, merged)
    weather_predictor(merged)
    pseudo_clock(merged)
    pseudo_clock_NN(merged)
    

if __name__ == '__main__':
    main()