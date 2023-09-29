import pandas_datareader as web
from datetime import datetime
import yfinance as yf
import talib as ta
import pandas as pd
import os.path


def createFile(fileName):
    if not os.path.exists("output"):
        os.mkdir("output")

    path = "output/" + fileName;
    if (os.path.isfile(path)):
        os.remove(path)

    with open(path, 'x') as f:
        print(fileName + " file created");
        return f.name

    return ""


def calculateWeeklyRsi(stock, start, end, outputFile):
    yf.pdr_override()
    print("----------------------" + stock + "--------------------------------------")
    data = web.data.get_data_yahoo(stock, start=start, end=end,
                                   interval='1wk')  # interval=1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

    data.index.name = 'Date'
    data.shape
    data['Rsi'] = ta.RSI(data['Close'], timeperiod=14)

    maxes = data[['High', 'Rsi']].max()
    lastValueOfHigh = data['High'].iat[-1]
    lastValueOfRsi = data['Rsi'].iat[-1]

    # Indexes are dates idxmax returns date of high and rsi
    maxValueDates = data.idxmax()

    dateFormat = "%Y-%m-%d"

    print(f'High: {maxValueDates["High"]} Rsi:{maxValueDates["Rsi"]}')

    if str(maxValueDates['High']) != 'NaT' and \
            str(maxValueDates['Rsi']) != 'NaT' and \
            str(maxValueDates['High']) != 'NaN' and \
            str(maxValueDates['Rsi']) != 'NaN':

        dateDiffOfMaxes = maxValueDates["Rsi"] - maxValueDates["High"]
        print(f'Difference: {dateDiffOfMaxes.days}')

        # Close max iken rsi da max olacak
        # Son fiyat max fiyattan küçük olacak ve rsi da max rsidan küçük olacak
        if -2 <= dateDiffOfMaxes.days <= 2 and lastValueOfHigh < maxes['High'] and lastValueOfRsi < maxes['Rsi']:
            print(f"-->Matching condition for  {stock} "
                  f"maxValueIndex['High']:{maxValueDates['High']} maxValueIndex['Rsi']:{maxValueDates['Rsi']}"
                  f"lastValueOfHigh:{lastValueOfHigh} maxes['High']:{maxes['High']} "
                  f"lastValueOfRsi:{lastValueOfRsi} maxes['Rsi']:{maxes['Rsi']}")
            with open(outputFile, 'a') as f:
                f.write(stock + "\n")


start = datetime(2019, 1, 1)
end = datetime.now()
df = pd.read_csv("resources/nasdaq.csv")

outputFile = createFile("nasdaq100.txt")
print(outputFile)
print(len(df))

if outputFile != "":
    for i, row in df.iterrows():
        if str(row["Industry"]) != 'nan':
            calculateWeeklyRsi(row["Symbol"], start, end, outputFile)
