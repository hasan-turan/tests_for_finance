import config
from data_providers import yahoo
from indicators import BollingerBand, IntradayIntensityIndex
from models import Pair, Stock

pair = Pair(base=Stock(title="TR", balance=100), counter=Stock("GOKNR.IS"))
data = yahoo.get_data(pair.counter.title, config.START_TIME, config.END_TIME, config.INTERVAL)

bb = BollingerBand(pair, config.INTERVAL, data)

iii = IntradayIntensityIndex(pair, config.INTERVAL, data)

print(bb.upper)


print(iii.get_line(0).get_data())