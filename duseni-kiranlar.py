import yfinance as yf
from datetime import datetime, timedelta
from utils.bist_utils import getBistStocks

# Tarih aralığı: son 10 gün
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# BIST 100 hisse senetleri sembolleri
 

stocks= getBistStocks()
bist_100_stocks= [stock.replace('\n', '').replace('\r', '')+".IS" for stock in stocks]


 
dipping_stocks = []

for stock_symbol in bist_100_stocks:
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    if len(stock_data) >= 5:  # En az 5 günlük veri olmalı
        if all(stock_data['Close'][-5:] > stock_data['Close'][-6]):  # Son 5 kapanış fiyatı öncekine göre düşüşte mi?
            dipping_stocks.append(stock_symbol)

print("Günlük periyotta düşeni kıran hisseler:", dipping_stocks)