import data_getter as dg
import utils
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


def weather_predictor(df, do_print=False):
    """
    This function creates a DecisionTreeClassifier that predicts the weather
    tag using the data from the trail dataset, if do_print is True, will
    summary results
    """
    df = df.dropna()
    X = df.loc[:, 'Total':'DAY_OF_WEEK']  # (df.columns != 'weather')] #
    y = df['weather']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    y_train = y_train.to_numpy(dtype=str)
    y_test = y_test.to_numpy(dtype=str)
    if do_print:
        print('weather_predictor')
        print('training set error rate: ' +
              str(100 * utils.error_rate(y_train, y_pred_train)) + '%')
        print('test set error rate: ' +
              str(100 * utils.error_rate(y_test, y_pred_test)) + '%')


def main():
    trail_df, weather_df = dg.get_data()
    merged = dg.merge_dataframes(trail_df, weather_df)
    utils.print_heads(trail_df, weather_df, merged)
    weather_predictor(merged, True)


if __name__ == '__main__':
    main()
