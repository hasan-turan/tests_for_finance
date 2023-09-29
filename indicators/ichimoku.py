from matplotlib.axes import Axes
from pandas import DataFrame

from enums import Interval
from models import Indicator, Pair, Trend, IndicatorLine
import matplotlib.pyplot as plt


class Ichimoku(Indicator):

    def __init__(self,
                 pair: Pair,
                 interval: Interval,
                 data: DataFrame,
                 trend: Trend = None,
                 **kwargs: None
                 ):

        self.tenkan_sen = None
        self.kijun_sen = None
        self.chikou_span = None
        self.senko_span_a = None
        self.senko_span_b = None

        self.tenkan_sen_period = 9
        self.kijun_sen_period = 26
        self.senko_span_b_period = 52
        self.displacement = 26
        if len(kwargs) > 0:
            if kwargs["tenkan_sen_period"] is not None:
                self.tenkan_sen_period = kwargs["tenkan_sen_period"]
            if kwargs["kijun_sen_period"] is not None:
                self.kijun_sen_period = kwargs["kijun_sen_period"]
            if kwargs["senko_span_b_period"] is not None:
                self.senko_span_b_period = kwargs["senko_span_b_period"]
            if kwargs["displacement"] is not None:
                self.displacement = kwargs["displacement"]

        super().__init__('Ichimoku', pair, interval, data, trend)

    def calculate(self):
        # Define Ichimoku Cloud parameters

        # Calculate the Ichimoku Cloud components
        self.tenkan_sen = (self.data['high'].rolling(window=self.tenkan_sen_period).max() +
                           self.data['low'].rolling(window=self.tenkan_sen_period).min()) / 2

        self.kijun_sen = (self.data['high'].rolling(window=self.kijun_sen_period).max() +
                          self.data['low'].rolling(window=self.kijun_sen_period).min()) / 2

        self.senko_span_a = (self.tenkan_sen + self.kijun_sen) / 2

        self.senko_span_b = (self.data['high'].rolling(window=self.senko_span_b_period).max() +
                             self.data['low'].rolling(window=self.senko_span_b_period).min()) / 2

        # Shift the cloud forward
        self.senko_span_a = self.senko_span_a.shift(self.displacement)
        self.senko_span_b = self.senko_span_b.shift(self.displacement)

        # Calculate the Chikou Span (Lagging Span)
        self.chikou_span = self.data['close'].shift(-self.displacement)

    def back_test(self, print_to_console: bool = False):
        pass

    def optimize(self, **kwargs: object):
        pass

    def plot(self, axes: Axes = None):
        fig, ax = plt.subplots(figsize=(12, 6))

        if axes is not None:
            ax = axes

        ax.plot(self.data.index, self.data['close'], label='Stock Price', alpha=0.7)

        # Plot the Ichimoku Cloud components
        ax.plot(self.data.index, self.senko_span_a, linestyle='-', label="Senko Span-a", color="lightblue")
        ax.plot(self.data.index, self.senko_span_b, linestyle='-', label="Senko Span-b", color="darkblue")

        ax.fill_between(self.data.index, self.senko_span_a, self.senko_span_b, where=(self.senko_span_a > self.senko_span_b), color='lightblue', alpha=0.5,
                        label='Ichimoku Cloud')
        ax.plot(self.data.index, self.tenkan_sen, label='Tenkan-Sen', linestyle='--', alpha=0.7, color="green")
        ax.plot(self.data.index, self.kijun_sen, label='Kijun-Sen', linestyle='--', alpha=0.7, color="red")

        ax.plot(self.data.index, self.chikou_span, label='Chikou Span', linestyle='-', alpha=0.7, color="cyan")

        ax.set_title(f'{self.pair.counter.title}/{self.pair.base.title} Stock Price with Ichimoku Cloud')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)
        # Show the plot
        plt.show()
