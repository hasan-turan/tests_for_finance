from typing import List

from indicators import AlphaTrend
from models.time_limit import TimeLimit
from utils import file_utils, bist_utils, crypto_utils, charting_utils, nasdaq_utils
from data_providers import yahoo, coinmarketcap, nasdaq
from utils.bist_utils import get_bist_stocks
from datetime import datetime, timedelta

from models import Order, Stock, Pair, Scale, Trend
from models import Portfolio
from enums import OrderSide, Interval


# def find_purchasable_stocks(orders: List[Order], limit, output_file_path):
#     if len(orders) > 0 and orders[-1].side == OrderSide.BUY and orders[-1].operation_date_diff.total_seconds() <= limit:
#         message = f"BUY-->Stock:{orders[-1].counter} Date:{orders[-1].date} Price:{orders[-1].price}"
#         print(message)
#         file_utils.write(output_file_path, message)
#
#
# def find_all_bist_shares_by_alpha_trend(start_date: datetime, end_date: datetime, interval: Interval, limit: int):
#     bist_stocks = get_bist_stocks("resources/bist_all")
#     output_file_path = "output/bist_all.txt"
#     file_utils.delete(output_file_path)
#     portfolio = Portfolio(10000.0)
#     base_stock = Stock("TL", 10000)
#     for s in bist_stocks:
#         counter_stock = Stock(s)
#         data = yahoo.get_data(counter_stock.title, start, end, interval)
#         pair = Pair(base_stock, counter_stock)
#         alpha_trend = AlphaTrend(pair, interval, data)
#         orders = alpha_trend.back_test(True)
#         pair.add_orders(orders)
#         portfolio.add_pair(pair)
#
#     portfolio.calculate_profit_or_loss()


# alpha_trend_tests.sort(key=lambda x: x.pair.profit_or_loss, reverse=True)
# for alpha_trend in alpha_trend_tests[5:]:
#     print(alpha_trend.pair.to_string())


# alpha_trend_2 = AlphaTrend(pair, interval, data)
# orders2 = alpha_trend_2.optimize(coefficient=Scale(1, 1, 1), active_period=Scale(2, 14, 1))


def test_crypto_all(print_to_console: bool = False, buy_limit: TimeLimit = None, sell_limit: TimeLimit = None):
    crypto_stock_list = crypto_utils.get_cryptos("resources/crypto.txt")
    test_for_stocks("USD", [c + "-USD" for c in crypto_stock_list], start, end, interval, print_to_console, buy_limit, sell_limit)


def test_nasdaq_all(print_to_console: bool = False, buy_limit: TimeLimit = None, sell_limit: TimeLimit = None):
    nasdaq_stock_list = nasdaq_utils.get_nasdaq_stocks()
    test_for_stocks("USD", nasdaq_stock_list, start, end, interval, print_to_console, buy_limit, sell_limit)


def test_bist_all(print_to_console: bool = False, buy_limit: TimeLimit = None, sell_limit: TimeLimit = None):
    bist_stock_list = bist_utils.get_bist_stocks()
    test_for_stocks("TL", bist_stock_list, start, end, interval, print_to_console, buy_limit, sell_limit)


def test_for_stocks(base_stock_title: str,
                    counter_stocks_list: List[str],
                    start,
                    end,
                    interval,
                    print_to_console: bool = False,
                    buy_limit: TimeLimit = None,
                    sell_limit: TimeLimit = None):
    alpha_trend_tests: List[AlphaTrend] = []
    print(f"Total stocks count:{len(counter_stocks_list)}")
    for index, counter_stock_title in enumerate(counter_stocks_list):
        print(f" Testing:{len(counter_stocks_list)}/{index} Stock:{counter_stock_title}")
        alpha_trend_tests.append(test_for_stock(start, end, interval, base_stock_title, counter_stock_title, None, print_to_console))

    if buy_limit is not None:
        print(f"-->Stocks that alpha trend gave BUY signal in {buy_limit.to_string()}")
        for alpha_trend in alpha_trend_tests:
            pair_title = alpha_trend.pair.get_last_buy_in(buy_limit)
            if pair_title != '':
                print(pair_title)

    if sell_limit is not None:
        print(f"-->Stocks that alpha trend gave SELL signal in {sell_limit.to_string()}")
        for alpha_trend in alpha_trend_tests:
            pair_title = alpha_trend.pair.get_last_sell_in(sell_limit)
            if pair_title != '':
                print(pair_title)

    print("-->Top 5 stocks that are most profitable ")
    sorted_alpha_trend_tests = sorted(alpha_trend_tests, key=lambda x: x.pair.profit_or_loss, reverse=True)
    for alpha_trend in sorted_alpha_trend_tests[:5]:
        print(alpha_trend.pair.to_string())


def optimize_for_stock(start: datetime, end: datetime,
                       interval: Interval,
                       base_stock_title: str,
                       counter_stock_title: str,
                       trend: Trend = None) -> AlphaTrend:
    base_stock = Stock(base_stock_title, 100)
    counter_stock = Stock(counter_stock_title, 0.0)
    pair = Pair(base_stock, counter_stock)
    data = yahoo.get_data(counter_stock.title, start, end, interval)

    # trend_utils.get_trend_change_mean(data)

    alpha_trend = AlphaTrend(pair, interval, data, trend)
    alpha_trend.optimize(coefficient=Scale(1, 10, 1), active_period=Scale(2, 28, 1))

    # charting_utils.plot_line_chart(data, [alpha_trend])
    return alpha_trend


def test_for_stock(start: datetime, end: datetime,
                   interval: Interval,
                   base_stock_title: str,
                   counter_stock_title: str,
                   trend: Trend = None,
                   print_to_console: bool = False) -> AlphaTrend:
    base_stock = Stock(base_stock_title, 100)
    counter_stock = Stock(counter_stock_title, 0.0)
    pair = Pair(base_stock, counter_stock)
    data = yahoo.get_data(counter_stock.title, start, end, interval)

    # trend_utils.get_trend_change_mean(data)

    alpha_trend = AlphaTrend(pair, interval, data, trend)
    alpha_trend.back_test(print_to_console)

    # charting_utils.plot_line_chart(data, [alpha_trend])
    return alpha_trend


def test_stock_with_title(stock_title: str):
    test_for_stock(start, end, interval, "USD", stock_title)


# start = datetime(2021, 9, 1)
end = datetime.now()
start = end - timedelta(days=729)
interval = Interval.i_1d

# optimize_for_stock(start, end, interval, "USD", "BTC-USD")
# test_for_stock(start, end, interval, "USD", "BTC-USD")

#


# test_nasdaq_all(buy_limit=TimeLimit(week=0,day=0,hour=24))
# test_crypto_all(buy_limit=TimeLimit(week=0,day=0,hour=24))
test_bist_all(buy_limit=TimeLimit(weeks=2))
