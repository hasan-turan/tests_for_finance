import pandas as pd

from utils import file_utils


def csv_to_txt():
    df = pd.read_csv("resources/nasdaq.csv")
    for i, row in df.iterrows():
        print(f' Industry: {row["Industry"]} Symbol: {row["Symbol"]}')
        if str(row["Industry"]) != 'nan' and str(row["Symbol"]) != 'nan':
            file_utils.append("resources/nasdaq_all.txt", row["Symbol"])


def get_nasdaq_stocks():
    lines = file_utils.read_lines("resources/nasdaq100.txt")
    stocks = []
    for line in lines:
        if len(line.strip()) > 0:
            stocks.append(line.replace("\r", "").replace("\n", ""))

    return stocks
