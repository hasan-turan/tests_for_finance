from statsmodels.tsa.stattools import adfuller
from pandas import DataFrame
import statsmodels.api as sm
import numpy as np

from enums import TrendDirection


def calculate_stationary(data: DataFrame):
    if len(data) < 4:
        return -1

    result = adfuller(data, autolag="AIC")
    p_value = result[1]
    # output_df = DataFrame({"Values": [augmented_dickey_fuller[0],
    #                                   augmented_dickey_fuller[1],
    #                                   augmented_dickey_fuller[2],
    #                                   augmented_dickey_fuller[3],
    #                                   augmented_dickey_fuller[4]['1%'],
    #                                   augmented_dickey_fuller[4]['5%'],
    #                                   augmented_dickey_fuller[4]['10%']],
    #                        "Metric": ["Test Statistics",
    #                                   "p-value",
    #                                   "No. of lags used",
    #                                   "Number of observations used",
    #                                   "critical value (1%)",
    #                                   "critical value (5%)",
    #                                   "critical value (10%)"]})

    # return output_df["Values"][1]
    return p_value


def trend_direction(data) -> TrendDirection:
    if len(data) < 4:
        return TrendDirection.NONE

    X = [i for i in range(0, len(data))]

    X = sm.add_constant(X)

    Y = data

    model = sm.OLS(Y, X).fit()
    slope = model.params[1]

    if slope > 0:
        return TrendDirection.UP
    elif slope < 0:
        return TrendDirection.DOWN
    else:
        return TrendDirection.NONE


def has_trend(data: DataFrame):
    p_value = calculate_stationary(data)
    # if p_value < 0.05 no trend (stationary) else there is a trend(non-stationary)
    return p_value > 0.05
