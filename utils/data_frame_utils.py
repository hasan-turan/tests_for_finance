from datetime import datetime

import pandas as pd


def to_4h_data(data):
    data_4h = to_hourly_data(data, 4)
    return data_4h


def to_hourly_data(df, hours):
    column_names = ["datetime", "open", "high", "low", "close", "adj_close", "volume"]
    result_df = pd.DataFrame(columns=column_names)

    current_index = 0
    current_low = 1000000000
    current_high = 0.0
    total_vol = 0.0
    open = 0.0
    date: datetime = None

    for row in df.iterrows():
        row = row[1]
        date = row['datetime']

        if current_index < hours:
            if current_index == 0:
                open = row['open']
            if row['low'] < current_low:
                current_low = row['low']
            if row['high'] > current_high:
                current_high = row['high']
            total_vol = total_vol + row['volume']
            current_index = current_index + 1
        else:
            close = row['close']
            adj_close = row['adj_close']
            new_row = [date, open, current_high, current_low, close, adj_close, total_vol]
            result_df = pd.concat([pd.DataFrame([new_row], columns=result_df.columns), result_df], ignore_index=True)
            open = 0.0
            current_index = 0
            current_low = 10000000000000000
            current_high = 0.0
            total_vol = 0.0
    return result_df
