from datetime import datetime

from data_providers import yahoo
from enums import Interval
from indicators import AlphaTrend
from models import Pair, Stock
from utils import crypto_utils

start = datetime(2019, 1, 1)  # end - timedelta(days=4*360)  #
end = datetime.now()
interval = Interval.i_1d
cryptos = crypto_utils.get_cryptos("resources/crypto.txt");

for crypto in cryptos:
    base_stock = Stock("USD", 1000)
    counter_stock = Stock(crypto)

    data = yahoo.get_data(counter_stock.title + "-USD", start, end, interval)
    pair = Pair(base_stock, counter_stock)

    alpha_trend = AlphaTrend(pair, interval,data)
    alpha_trend.back_test(print_to_console=True)
