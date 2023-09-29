import copy
from typing import List

import matplotlib.pyplot as plt

import pandas as pd

from enums.line_styles import LineStyle
from models import Indicator


def plot_line_chart(data: pd.DataFrame, indicators: List[Indicator] = None):
    x = pd.to_datetime(data["datetime"])
    y = data["close"]
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linestyle=LineStyle.SOLID.value, label='Price')
    for indicator in indicators:
        for line in indicator.get_lines():
            plt.plot(x, line.get_data(), linestyle=line.line_style.value, label=f'{indicator.title}({line.title})', color=line.color)

        for signal in indicator.get_signals():
            plt.scatter(x[signal.index], y[signal.index], label=signal.label, color=signal.color, marker=signal.marker, s=100)

    plt.grid(True)
    plt.show()
# def create_chart_3(stock, data, indicators: [Indicator]) -> None:
#     add_plot = []
#
#     for indicator in indicators:
#         add_plot.append(mplf.make_addplot(data=indicator.data,
#                                           color=indicator.color,
#                                           width=indicator.width,
#                                           title=indicator.title,
#                                           linestyle=indicator.line_style))
#     mplf.plot(data,
#               type="candle",
#               style="charles",
#               addplot=add_plot,
#               # mav=(21,50,100),
#               title=stock,
#               ylabel="Price",
#               volume=True,
#               ylabel_lower='Shares\nTraded',
#               show_nontrading=True
#               )
#
#
# def create_web_chart(stock, data, k1, k2):
#     dates = data.index.tolist()
#     candlestick_trace = go.Candlestick(
#         x=dates,
#         open=data['open'],
#         high=data['high'],
#         low=data['low'],
#         close=data['close'],
#         increasing_line_color='green',
#         decreasing_line_color='red'
#     )
#
#     indicator_trace_k1 = go.Scatter(
#         x=dates,
#         y=k1,
#         mode='lines',
#         line=dict(color='green')
#     )
#
#     indicator_trace_k2 = go.Scatter(
#         x=dates,
#         y=k2,
#         mode='lines',
#         line=dict(color='red')
#     )
#
#     layout = go.Layout(
#         title=f'{stock}',
#         xaxis=dict(title='Date'),
#         yaxis=dict(title='Price'),
#         showlegend=False
#     )
#
#     figure = go.Figure(data=[candlestick_trace, indicator_trace_k1, indicator_trace_k2], layout=layout)
#     figure.show()
#
#
# def create_chart(stock, data, indicators, interval, plot_rsi=True):
#     figure, axis = plt.subplots(2, 1, figsize=(16.5, 12.5), sharex=True, sharey=False,
#                                 gridspec_kw={'height_ratios': [6, 2]})
#
#     ohlc = data.loc[::, ['open', 'high', 'low', 'close']]
#     ohlc['date'] = data.index.values
#     ohlc['date'] = pd.to_datetime(ohlc['date'])
#
#     ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
#
#     ohlc = ohlc.astype(float)
#     candlestick_ohlc(axis[0], ohlc.values, width=0.6, colorup='green', colordown='red',
#                      alpha=0.8)
#
#     figure.suptitle(f'Candlestick Chart of {stock} ({interval})')
#
#     axis[0].legend(loc="upper left")
#
#     for indicator in indicators:
#         axis[0].plot(indicator, linewidth=5)
#
#     if plot_rsi is True:
#         rsi = ta.RSI(data["close"], timeperiod=14)
#         axis[1].plot(rsi, label="rsi", linewidth=2)
#         axis[1].axhline(y=70, color='g', linestyle="dashed", linewidth=2)
#         axis[1].axhline(y=30, color='g', linestyle="dashed", linewidth=2)
#
#     figure.tight_layout()
#     plt.show()
