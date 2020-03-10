from data_getter import DataGetter
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor


def pseudo_clock(df):
    df = df.dropna()
    X = df.loc[:, (df.columns != 'HOUR')]
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
    error_analysis(y_test, y_pred_test)



def pseudo_clock_NN(df):
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
    error_analysis(y_test, y_pred_test)


def error_analysis(true, pred):
    true = true.to_numpy()
    total = 0
    # res = {i:[0,0] for i in range(1, 25)}
    for (tr, pred) in zip(true, pred):
        if abs(tr-pred) < 0.5:
            total += 1
            # res[tr][0] += 1
        # res[tr][1] += 1
    # res = {k:(val[0]/val[1]) for k, val in res.items() if val[0] > 0}
    print(f'total: {total} proprotion: {total/len(true)}')
    # for k in res:
        # print(f'hour {k}: {res[k]} correct')


def main():
    data_getter = DataGetter()
    trail_df, weather_df = data_getter.get_data()
    merged = data_getter.merge_dataframes(trail_df, weather_df)
    # utils.print_heads(trail_df, weather_df, merged)
    print('merged data')
    pseudo_clock(merged)
    pseudo_clock_NN(merged)
    # print('trail data')
    # pseudo_clock(trail_df)
    # pseudo_clock_NN(trail_df)


if __name__ == '__main__':
    main()
