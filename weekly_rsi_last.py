import pandas_datareader as web
from datetime import datetime
import yfinance as yf
import talib as ta

from enums import Interval
from indicators import inconsistency


def calculateWeeklyRsi(stock, start, end):
    yf.pdr_override()
    data = web.data.get_data_yahoo(stock, start=start, end=end, interval='1wk')  # interval=1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

    data.index.name = 'Date'
    data.shape
    data['Rsi'] = ta.RSI(data['Close'], timeperiod=14)

    maxes = data[['High', 'Rsi']].max()
    lastValueOfHigh = data['High'].iat[-1]
    lastValueOfRsi = data['Rsi'].iat[-1]

    # Indexes are dates idxmax returns date of high and rsi
    maxValueDates = data.idxmax()

    # print(f'High: {maxValueDates["High"]} Rsi:{maxValueDates["Rsi"]}')

    if (str(maxValueDates['High']) != 'NaT' and str(maxValueDates['Rsi']) != 'NaT'):

        dateDiffOfMaxes = maxValueDates["Rsi"] - maxValueDates["High"]
        # print(f'Difference: {dateDiffOfMaxes.days}')

        # Close max iken rsi da max olacak
        # Son fiyat max fiyattan küçük olacak ve rsi da max rsidan küçük olacak
        if (-2 <= dateDiffOfMaxes.days <= 2) and lastValueOfHigh < maxes['High'] and lastValueOfRsi < maxes['Rsi']:
            print(f"-->Matching condition for  {stock} "
                  f"maxValueIndex['High']:{maxValueDates['High']} maxValueIndex['Rsi']:{maxValueDates['Rsi']}"
                  f"lastValueOfHigh:{lastValueOfHigh} maxes['High']:{maxes['High']} "
                  f"lastValueOfRsi:{lastValueOfRsi} maxes['Rsi']:{maxes['Rsi']}")


start = datetime(2019, 1, 1)
end = datetime.now();
# f = open("resources/bist100", "r")
# stocks = f.readlines()
# f.close()

# for stock in stocks:
#     if(len(stock.strip())>0):
#         stockNameForYahoo=stock.replace("\n","")+".IS"
#         calculateWeeklyRsi(stockNameForYahoo,start,end)

# stocks = bist.get_bist_stocks("resources/bist_100")
# for stock in stocks:
#     data = yahoo.get_yahoo_data(stock, start, end, Interval.i_1wk)
#     inconsistency.calculate_inconsistency(stock, data)

data = yahoo.get_data("IZMDC.IS", start, end, Interval.i_1wk)
inconsistency.calculate_inconsistency("IZMDC.IS", data)
