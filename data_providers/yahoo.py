import yfinance as yf
import pandas_datareader as web


from enums import Interval


# interval=1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
def get_data(stock, start, end, interval: Interval):
    yf.pdr_override()
    data = web.data.get_data_yahoo(stock, start=start, end=end, interval=interval.value)
    data = data[['Open', 'High', 'Low', 'Close', "Adj Close", 'Volume']]
    data = data.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'})

    data.insert(loc=0, column="datetime", value=data.index.tolist())
    data = data.reset_index(drop=True)
    data.shape

    return data




