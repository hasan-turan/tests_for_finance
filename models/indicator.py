from abc import ABC, abstractmethod
from typing import List, Any, Generator

from pandas import DataFrame

from enums import Interval
from models import Stock, Pair, Order, Trend
from models.indicator_line import IndicatorLine
from models.signal import Signal


class Indicator(ABC):

    def __init__(self,
                 title: str,
                 pair: Pair,
                 interval: Interval,
                 data: DataFrame,
                 trend: Trend = None
                 ):
        self.title = title
        self.pair = pair
        self.interval = interval
        self.data = data
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.volume = data["volume"]
        self.datetime = data["datetime"]
        self.value = None

        self.__lines: List[IndicatorLine] = []
        self.__signals: List[Signal] = []
        self.calculate()

    def add_signal(self, signal: Signal):
        self.__signals.append(signal)

    def clear_signals(self):
        self.__signals.clear()

    def get_signals(self):
        return self.__signals

    def get_signal(self, index) -> Signal:
        return next(
            (signal for i, signal in enumerate(self.__signals) if i == index),
            None
        )

    def add_line(self, line: IndicatorLine):
        self.__lines.append(line)

    def get_lines(self) -> List[IndicatorLine]:
        return self.__lines

    def remove_lines(self):
        self.__lines.clear()

    def get_line(self, title: str) -> IndicatorLine:
        return next(
            (obj for obj in self.__lines if obj.title == title),
            None
        )

    def get_line(self, index: int) -> IndicatorLine:
        return self.__lines[index]

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def back_test(self, print_to_console: bool = False):
        pass

    @abstractmethod
    def optimize(self, **kwargs: object):
        pass
