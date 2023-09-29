from typing import List
import pandas as pd
import copy
import math
import talib as ta
from pandas import DataFrame

from enums import Interval, OrderSide, TrendDirection
from models import Indicator
from models import Order, Stock, Pair, Scale, Portfolio, ProfitLoss, Parameter, Trend
from models.indicator_line import IndicatorLine
from models.signal import Signal
from utils import adf_utils
import numpy as np


class AlphaTrend(Indicator):

    def __init__(self,
                 pair: Pair,
                 interval: Interval,
                 data: DataFrame,
                 trend: Trend = None
                 ):
        super(AlphaTrend, self).__init__('Alpha Trend', pair, interval, data, trend)

        self.coefficient = 1
        self.active_period = 14
        self.no_volume_data = False

    def back_test(self, print_to_console: bool = False):

        if len(self.data) == 0:
            print(f'No data found for stock :{self.pair.counter.title}')
            return self.pair.get_orders()

        self.calculate()

        date = self.data["datetime"].values
        self.pair.data_start_time = date[0]
        self.pair.data_end_time = date[-1]
        price = self.data["close"].values

        k1 = self.get_line("k1")
        k2 = self.get_line("k2")
        k1_data = k1.get_data()
        k2_data = k2.get_data()

        self.pair.clear_orders()
        p_value = 0.0
        for i in range(1, len(k1_data)):
            signal_order = self.pair.get_orders()[-1].side if len(self.pair.get_orders()) > 0 else OrderSide.SELL
            if k1_data[i - 1] <= k2_data[i - 1] and k1_data[i] > k2_data[i] and signal_order != OrderSide.BUY:

                trend_direction = TrendDirection.UP
                if self.trend is not None:
                    trend_direction = adf_utils.trend_direction(price[i - self.trend.period:i])
                    print(f"i:{i} Date:{date[i]} Price: {price[i - self.trend.period:i]} "
                          f"len:{len(price[i - self.trend.period:i])}"
                          f"price[i]:{price[i]} "
                          f"x:{price[i - self.trend.period:i][self.trend.period - 1] if i > self.trend.period else ''}")

                if trend_direction == TrendDirection.UP:
                    self.add_signal(Signal(i, "BUY", "*", "green"))
                    quantity = (self.pair.base.balance / price[i])
                    order = Order(
                        self.pair.base.title,
                        self.pair.counter.title,
                        OrderSide.BUY,
                        date[i],
                        price[i],
                        quantity,
                        price[-1],
                        self.interval)
                    self.pair.add_order(order)

            elif k1_data[i - 1] >= k2_data[i - 1] and k1_data[i] < k2_data[i] and signal_order != OrderSide.SELL:
                self.add_signal(Signal(i, "SELL", "*", "red"))
                order = Order(
                    self.pair.base.title,
                    self.pair.counter.title,
                    OrderSide.SELL,
                    date[i],
                    price[i],
                    self.pair.get_orders()[-1].quantity,
                    price[-1],
                    self.interval
                )
                self.pair.add_order(order)

        if print_to_console is True:
            print(self.pair.to_string(), end="\n")

    def optimize(self, coefficient: Scale, active_period: Scale):
        profit_or_losses: List[ProfitLoss] = []

        coefficient_repeat_count = (coefficient.end - coefficient.start) / coefficient.step
        active_period_repeat_count = (active_period.end - active_period.start) / active_period.step
        total_repeat_count = coefficient_repeat_count * active_period_repeat_count
        print(f"Total Repeat Count:{total_repeat_count}")
        count = 0
        for i in np.arange(coefficient.start, coefficient.end + coefficient.step, coefficient.step):
            for j in np.arange(active_period.start, active_period.end + coefficient.step, active_period.step):
                self.pair.reset()
                self.coefficient = i
                self.active_period = j

                count += 1
                print(f"Total Repeat Count:{total_repeat_count}/{count} -> Coefficient:{self.coefficient} Active Period:{self.active_period}")

                self.back_test(False)

                # print(f"self.coefficient:{self.coefficient} self.active_period:{self.active_period} \n",end="\n")
                # print(self.pair.to_string())
                profit_or_loss = ProfitLoss(pair=copy.deepcopy(self.pair),
                                            parameters=[Parameter("coefficient", self.coefficient),
                                                        Parameter("active_period", self.active_period)]
                                            )

                profit_or_losses.append(profit_or_loss)

        sorted_profit_or_losses = sorted(profit_or_losses, key=lambda x: x.pair.profit_or_loss, reverse=True)

        for p_l in sorted_profit_or_losses[:5]:
            print(p_l.to_string(), end="\n")

        # print("***" * 50)
        # for p_l in profit_or_losses:
        #     print(p_l.to_string(), end="\n")

    def calculate(self):
        try:
            self.remove_lines()

            k1 = IndicatorLine('k1', [], "green")
            k2 = IndicatorLine('k2', [], "red")

            self.add_line(k1)
            self.add_line(k2)

            open = self.data['open']
            close = self.data['close']
            high = self.data['high']
            low = self.data['low']
            volume = self.data['volume']

            alpha_trend = [0.0]

            tr = ta.TRANGE(high, low, close)
            atr = ta.SMA(tr, timeperiod=self.active_period)
            src = close
            rsi = ta.RSI(src, timeperiod=self.active_period)
            mfi = ta.MFI(high, low, close, volume, timeperiod=self.active_period)

            up_t = low - (atr * self.coefficient)
            down_t = high + (atr * self.coefficient)

            for i in range(1, len(close)):

                if self.no_volume_data is True and rsi[i] >= 50:
                    if up_t[i] < alpha_trend[i - 1]:
                        alpha_trend.append(alpha_trend[i - 1])
                    else:
                        alpha_trend.append(up_t[i])

                elif self.no_volume_data is False and mfi[i] >= 50:
                    if up_t[i] < alpha_trend[i - 1]:
                        alpha_trend.append(alpha_trend[i - 1])
                    else:
                        alpha_trend.append(up_t[i])
                else:
                    if down_t[i] > alpha_trend[i - 1]:
                        alpha_trend.append(alpha_trend[i - 1])
                    else:
                        alpha_trend.append(down_t[i])

            alpha_trend = [0.0 if math.isnan(x) else x for x in alpha_trend]

            for i in range(len(alpha_trend)):
                if i < 2:
                    k2.add_data_item(0)
                    k1.add_data_item(alpha_trend[i])
                else:
                    k2.add_data_item(alpha_trend[i - 2])
                    k1.add_data_item(alpha_trend[i])

        except Exception as e:
            print('Failed to upload to ftp: ' + str(e))
