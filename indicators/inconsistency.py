import talib as ta
from pandas import DataFrame, isna


def calculate_inconsistency(stock, data: DataFrame):
    data['rsi'] = ta.RSI(data['close'], timeperiod=14)

    last_high = data['high'].iat[-1]
    last_rsi = data['rsi'].iat[-1]

    row_index_of_maxes = data.idxmax()  # Find the row index which has the maximum value

    if isna(row_index_of_maxes["rsi"]) or isna(row_index_of_maxes["high"]):
        return

    print(row_index_of_maxes)

    max_high = data["high"][row_index_of_maxes["high"]]
    max_rsi = data["rsi"][row_index_of_maxes["rsi"]]
    date_of_max_high = data["datetime"][row_index_of_maxes["high"]]
    date_of_max_rsi = data["datetime"][row_index_of_maxes["rsi"]]


    date_diff_of_max_high_and_max_rsi = abs(date_of_max_high - date_of_max_rsi)

    # print(row_index_of_maxes)
    # print("*" * 10)
    # print(maxes)
    # print(f"last_high:{last_high} last_rsi:{last_rsi}")
    # print(f'max_high:{max_high} max_high date:{date_of_max_high} max_rsi:{max_rsi} date of max rsi:{date_of_max_rsi}')

    # print(f"-->Stock {stock} "
    #       f" Diff:{date_diff_of_max_high_and_max_rsi.days}"
    #       f"max_high:{max_high} max_rsi:{max_rsi}"
    #       f"last_high:{last_high} last_rsi:{last_rsi} "
    #       f"date_of_max_high:{date_of_max_high} date_of_max_rsi:{date_of_max_rsi}")
    # 7 *2 = weekly two candles
    if date_diff_of_max_high_and_max_rsi.days <= 7*2 and last_high < max_high and last_rsi < max_rsi:
        print(f"-->Matching condition for  {stock} "
              f"max_high:{max_high} max_rsi:{max_rsi}"
              f"last_high:{last_high} last_rsi:{last_rsi} "
              f"date_of_max_high:{date_of_max_high} date_of_max_rsi:{date_of_max_rsi}")
