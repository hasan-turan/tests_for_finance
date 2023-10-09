from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from enums import Interval
from indicators import AlphaTrend
from models import TimeLimit, Trend, Stock, Pair, Indicator, DataProvider
from utils import data_frame_utils, bist_utils, nasdaq_utils, crypto_utils


class Filter(ABC):

    def __init__(self, indicator: Indicator, data_provider: DataProvider):
        self.data_provider = data_provider
        self.indicator = indicator;

    def back_test_crypto_all(
            self,
            start: datetime,
            end: datetime,
            interval: Interval,
            print_to_console: bool = False,
            buy_limit: TimeLimit = None,
            sell_limit: TimeLimit = None):
        crypto_stock_list = crypto_utils.get_cryptos("resources/crypto.txt")
        back_test_for_stocks("USD", [c + "-USD" for c in crypto_stock_list], start, end, interval, print_to_console, buy_limit, sell_limit)


def back_test_nasdaq_all(self, start: datetime,
                         end: datetime,
                         interval: Interval,
                         print_to_console: bool = False,
                         buy_limit: TimeLimit = None,
                         sell_limit: TimeLimit = None):
    nasdaq_stock_list = nasdaq_utils.get_nasdaq_stocks()
    self.back_test_for_stocks("USD", nasdaq_stock_list, start, end, interval, print_to_console, buy_limit, sell_limit)


def back_test_bist_all(self,
                       start: datetime,
                       end: datetime,
                       interval: Interval,
                       print_to_console: bool = False,
                       buy_limit: TimeLimit = None,
                       sell_limit: TimeLimit = None):
    bist_stock_list = bist_utils.get_bist_stocks()

    self.back_test_for_stocks("TL", bist_stock_list, start, end, interval, print_to_console, buy_limit, sell_limit)


def back_test_for_stocks(
        self,
        base_stock_title: str,
        counter_stocks_list: List[str],
        start,
        end,
        interval,
        print_to_console: bool = False,
        buy_limit: TimeLimit = None,
        sell_limit: TimeLimit = None):
    back_tested_pairs: List[Pair] = []
    print(f"Total stocks count:{len(counter_stocks_list)}")
    for index, counter_stock_title in enumerate(counter_stocks_list):
        print(f" Testing:{len(counter_stocks_list)}/{index} Stock:{counter_stock_title}")
        back_tested_pairs.append(self.back_test_for_stock(start, end, interval, base_stock_title, counter_stock_title, None, print_to_console))

    if buy_limit is not None:
        print(f"-->Stocks that alpha trend gave BUY signal in {buy_limit.to_string()}")
        for back_tested_pair in back_tested_pairs:
            pair_title = back_tested_pair.get_last_buy_in(buy_limit)
            if pair_title != '':
                print(pair_title)

    if sell_limit is not None:
        print(f"-->Stocks that alpha trend gave SELL signal in {sell_limit.to_string()}")
        for back_tested_pair in back_tested_pairs:
            pair_title = back_tested_pair.get_last_sell_in(sell_limit)
            if pair_title != '':
                print(pair_title)

    print("-->Top 10 stocks that are most profitable ")
    sorted_alpha_trend_tests = sorted(back_tested_pairs, key=lambda x: x.pair.profit_or_loss, reverse=True)
    for back_tested_pair in sorted_alpha_trend_tests[:10]:
        print(back_tested_pair.pair.to_string())


def back_test_for_stock(self,
                        start: datetime,
                        end: datetime,
                        interval: Interval,
                        base_stock_title: str,
                        counter_stock_title: str,
                        trend: Trend = None,
                        print_to_console: bool = False) -> Pair:
    base_stock = Stock(base_stock_title, 100)
    counter_stock = Stock(counter_stock_title, 0.0)
    pair = Pair(base_stock, counter_stock)
    data = self.data_provider.get_data(counter_stock.title, start, end, Interval.i_1h if interval == Interval.i_4h else interval)
    if interval == Interval.i_4h:
        data = data_frame_utils.to_4h_data(data)

    self.indicator.set_pair(pair)
    self.indicator.set_interval(interval)
    self.indicator.set_data(data)
    self.indicator.set_trend(trend)

    return self.indicator.back_test(print_to_console)
