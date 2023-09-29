from pandas import DataFrame
from talib import MA_Type

from enums import Interval
from models import Indicator, Pair, Trend, IndicatorLine
import talib as ta


class BollingerBand(Indicator):

    def __init__(self,
                 pair: Pair,
                 interval: Interval,
                 data: DataFrame,
                 trend: Trend = None
                 ):
        self.lower = None
        self.upper = None
        self.middle = None
        super().__init__('Bollinger Band', pair, interval, data, trend)

    def back_test(self, print_to_console: bool = False):
        pass

    def optimize(self, **kwargs: object):
        pass

    def calculate(self):
        upper, middle, lower = ta.BBANDS(self.data["close"], timeperiod=12)
        self.upper = upper
        self.lower = lower
        self.middle = middle

        upper_line = IndicatorLine(self.title + "-upper", upper, "blue")
        self.add_line(upper_line)

        middle_line = IndicatorLine(self.title + "-upper", middle, "red")
        self.add_line(middle_line)

        lower_line = IndicatorLine(self.title + "-upper", middle, "blue")
        self.add_line(lower_line)
