import yfinance as yf
import mplfinance as mpf
import pandas as pd
# Define the stock symbol and date range
stock_symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2021-12-31'

# Fetch historical stock price data
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

# Create a DataFrame with Ichimoku Cloud components
ichimoku_cloud_data = pd.DataFrame({
    'Open': stock_data['Open'],
    'High': stock_data['High'],
    'Low': stock_data['Low'],
    'Close': stock_data['Close'],
    'Conversion Line': conversion_line,
    'Base Line': base_line,
    'Leading Span A': leading_span_a,
    'Leading Span B': leading_span_b,
    'Chikou Span': chikou_span
})


extra_plot = [
    mpf.make_addplot(ichimoku_cloud_data['Conversion Line'], color='orange', secondary_y=False),
    mpf.make_addplot(ichimoku_cloud_data['Base Line'], color='blue', secondary_y=False),
    mpf.make_addplot(ichimoku_cloud_data['Leading Span A'], color='green', secondary_y=False),
    mpf.make_addplot(ichimoku_cloud_data['Leading Span B'], color='red', secondary_y=False),
    mpf.make_addplot(ichimoku_cloud_data['Chikou Span'], color='purple', secondary_y=False)
]

# Plot the candlestick chart with the Ichimoku Cloud
mpf.plot(ichimoku_cloud_data, type='candle', addplot=extra_plot, style='yahoo', title=f'{stock_symbol} Stock Price with Ichimoku Cloud', ylabel='Price', figratio=(12, 6))