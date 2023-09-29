import datetime
import mplfinance as mpf
import yfinance as yf
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

# Define the list of stock symbols and date range
stock_symbol = 'PRKAB.IS'  # Add more stock symbols as needed
start_date = datetime.datetime(day=1, month=1, year=2017)
end_date = datetime.datetime.now()

stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Define Ichimoku Cloud parameters
conversion_line_period = 9
base_line_period = 26
leading_span_b_period = 52
displacement = 26

# Calculate the Ichimoku Cloud components
conversion_line = (stock_data['High'].rolling(window=conversion_line_period).max() +
                   stock_data['Low'].rolling(window=conversion_line_period).min()) / 2

base_line = (stock_data['High'].rolling(window=base_line_period).max() +
             stock_data['Low'].rolling(window=base_line_period).min()) / 2

leading_span_a = (conversion_line + base_line) / 2

leading_span_b = (stock_data['High'].rolling(window=leading_span_b_period).max() +
                  stock_data['Low'].rolling(window=leading_span_b_period).min()) / 2

# Shift the cloud forward
leading_span_a = leading_span_a.shift(displacement)
leading_span_b = leading_span_b.shift(displacement)

# Calculate the Chikou Span (Lagging Span)
chikou_span = stock_data['Close'].shift(-displacement)

# Create a plot
plt.figure(figsize=(12, 6))

# Plot the stock's price data
plt.plot(stock_data.index, stock_data['Close'], label='Stock Price', alpha=0.7)

# Plot the Ichimoku Cloud components
plt.plot(stock_data.index, leading_span_a, linestyle='-',label="Senko Span-a", color = "lightblue")
plt.plot(stock_data.index, leading_span_b, linestyle='-',label="Senko Span-b", color = "darkblue")

plt.fill_between(stock_data.index, leading_span_a, leading_span_b, where=(leading_span_a > leading_span_b), color='lightblue', alpha=0.5, label='Ichimoku Cloud')
plt.plot(stock_data.index, conversion_line, label='Tenkan-Sen', linestyle='--', alpha=0.7, color="green")
plt.plot(stock_data.index, base_line, label='Kijun-Sen', linestyle='--', alpha=0.7, color="red")

plt.plot(stock_data.index, chikou_span, label='Chikou Span', linestyle='-', alpha=0.7, color="cyan")

plt.title(f'{stock_symbol} Stock Price with Ichimoku Cloud')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
