from datetime import datetime
import pandas_datareader as web
import matplotlib.pyplot as plot
import matplotlib.dates as dates

import mplfinance as mpf
import yfinance as yf
import numpy as np
import pandas as pd
start= datetime(2019,1,1)

end=  datetime.now();
yf.pdr_override()

data=web.data.get_data_yahoo('BTC',start='2019-01-01',end='2023-07-28')

data=data[['Open','High','Low','Close','Volume']]

data.index.name='Date'
data.shape
mpf.plot(data,type='candle',mav=(7,12),volume=True,show_nontrading=True)
