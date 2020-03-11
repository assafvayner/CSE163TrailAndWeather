import data_getter as dg
import utils
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

# This is the file where we try to make a model to predict the time
# based on the number of bikers and pedestrians on the trail


def pseudo_clock(df):
    """
    Trains a DecisionTreeRegressor to predict the hour and reports
    summary of results
    """
    df = df.dropna()
    X = df.loc[:, (df.columns != 'HOUR')]
    y = df['HOUR']
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    print('pseudo_clock')
    print(f'training set MSE: {mean_squared_error(y_train, y_pred_train)}')
    print(f'test set MSE: {mean_squared_error(y_test, y_pred_test)}')


def pseudo_clock_NN(df):
    """
    Trains a Neural Network Regressor to predict the hour and reports
    summary of results
    """
    df = df.dropna()
    X = df.loc[:, df.columns != 'HOUR']  # 'Total':'Bike South']#
    y = df['HOUR']
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    num_hidden = 100
    model = MLPRegressor(num_hidden)
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    print('peudo_clock_NN with num_hidden: ' + str(num_hidden))
    error_train = mean_squared_error(y_train, y_pred_train)
    print(f'training set MSE: {error_train}')
    error_test = mean_squared_error(y_test, y_pred_test)
    print(f'test set MSE: {error_test}')


def main():
    trail_df, weather_df = dg.get_data()
    merged = dg.merge_dataframes(trail_df, weather_df)
    utils.print_heads(merged=merged)
    print('merged data')
    pseudo_clock(merged)
    pseudo_clock_NN(merged)
    print('trail data')
    pseudo_clock(trail_df)
    pseudo_clock_NN(trail_df)


if __name__ == '__main__':
    main()
