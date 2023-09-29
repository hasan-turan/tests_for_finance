import config
from data_providers import yahoo
from enums import OrderSide
from indicators import Ichimoku
from models import Pair, Stock, Order
from utils import bist_utils

bist_stocks = bist_utils.get_bist_stocks()
for bist_stock in bist_stocks:
    pair = Pair(base=Stock(title="TR", balance=100), counter=Stock(bist_stock))
    data = yahoo.get_data(pair.counter.title, config.START_TIME, config.END_TIME, config.INTERVAL)

    ichimoku = Ichimoku(pair, config.INTERVAL, data)
    signal_order = ['S']
    for i in range(0, len(ichimoku.data["close"])):
        close = ichimoku.data["close"][i]
        last_price = ichimoku.data["close"][-1:]
        date = ichimoku.data["datetime"][i]
        if ichimoku.tenkan_sen[i] > ichimoku.kijun_sen[i] and \
                close > ichimoku.senko_span_a[i] and \
                close > ichimoku.senko_span_b[i] and \
                ichimoku.chikou_span[i] > close and \
                signal_order[-1] == "S":
            # print(f"BUY {bist_stock} at price {ichimoku.data['close'][i]}")
            signal_order.append("B")
            buy_order = Order(pair.base.title, pair.counter.title, OrderSide.BUY, date, close, pair.base.balance / close, last_price, config.INTERVAL)
            pair.add_order(buy_order)
        elif ichimoku.tenkan_sen[i] < ichimoku.kijun_sen[i] and \
                close < ichimoku.senko_span_a[i] and \
                close < ichimoku.senko_span_b[i] and \
                ichimoku.chikou_span[i] < close and \
                signal_order[-1] == "B":
            #  print(f"SELL {bist_stock} at price {ichimoku.data['close'][i]}")
            sell_order = Order(pair.base.title, pair.counter.title, OrderSide.SELL, date, close, pair.get_orders()[-1].quantity, last_price, config.INTERVAL)
            pair.add_order(sell_order)
            signal_order.append("S")

    if len(pair.get_orders()) > 0:
        print(pair.to_string(), end="\n")
