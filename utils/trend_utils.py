from datetime import datetime

from pandas import DataFrame
import pandas


from enums import TrendDirection, Interval
import ruptures as rpt
import matplotlib.pyplot as plt
from data_providers import yahoo

def get_trend_change_mean(df: DataFrame):
    data = df['close'].values
    algo = rpt.Pelt(model="rbf").fit(data)
    result = algo.predict(pen=0.75)

    fig, ax = plt.subplots()
    ax.plot(data, color='tab:red')
    for r in result:
        ax.axvline(x=r, color='k', linestyle='--')

    plt.show()





# start = datetime(2017, 1, 1)
# end = datetime.now()
# interval = Interval.i_1d
# data = yahoo.get_data("BTC-USD", start, end, interval)
# get_trend_change_mean(data)