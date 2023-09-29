from pandas import DataFrame

from enums import Interval
from models import Indicator, Pair, Trend, IndicatorLine


class IntradayIntensityIndex(Indicator):

    def __init__(self,
                 pair: Pair,
                 interval: Interval,
                 data: DataFrame,
                 trend: Trend = None
                 ):
        super().__init__('Intraday Intensity Index', pair, interval, data, trend)

    def calculate(self):
        result = (2 * self.close - self.high - self.low) / (self.high - self.low)
        line = IndicatorLine(self.title + "-Value", result, "red")
        self.add_line(line)

    def back_test(self, print_to_console: bool = False):
        pass

    def optimize(self, **kwargs: object):
        pass
