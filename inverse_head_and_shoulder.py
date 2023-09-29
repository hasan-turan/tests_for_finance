from datetime import datetime

import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt

from data_providers import yahoo
from enums import Interval

# Load financial time series data (e.g., OHLCV data)
# Replace 'your_data.csv' with the path to your data file
start = datetime(2017, 1, 1)
end = datetime.now()

interval = Interval.i_1d

data = yahoo.get_data("BTC-USD", start, end, interval)

data['datetime'] = pd.to_datetime(data['datetime'])  # Convert 'Date' column to datetime

# Define the period for the pattern detection
# You can adjust this based on your data and requirements
period = 14  # Example: You can use a different value

# Calculate the required indicators for the pattern detection
data['SMA'] = talib.SMA(data['close'], timeperiod=period)
data['RSI'] = talib.RSI(data['close'], timeperiod=period)

# Detect the Inverse Head and Shoulders pattern
data['IHS'] = (
        (data['close'] > data['SMA']) &
        (data['RSI'] < 30) &  # RSI below 30 indicates potential reversal
        (data['close'].shift(1) > data['close']) &
        (data['close'].shift(2) > data['close']) &
        (data['close'].shift(-1) > data['close']) &
        (data['close'].shift(-2) > data['close'])
    # You can add more criteria specific to the IHS pattern
)

# Find the rows where the pattern is detected
inverse_head_shoulders = data[data['IHS']]

# Create a chart with the detected pattern
plt.figure(figsize=(12, 6))
plt.plot(data['datetime'], data['close'], label='Price', color='blue')
plt.scatter(
    inverse_head_shoulders['datetime'],
    inverse_head_shoulders['close'],
    label='Inverse Head & Shoulders',
    color='green',
    marker='^',
    s=100,
)
plt.title('Inverse Head & Shoulders Pattern Detection')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# Print the rows where the pattern is found
print(inverse_head_shoulders)

