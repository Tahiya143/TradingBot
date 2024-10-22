import yfinance as yf
from datetime import time,datetime,timedelta
asset = yf.Ticker("AMZN")
start_date = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
df = asset.history(start=start_date, interval='1m')
del df['Dividends']
del df['Stock Splits']
del df['Volume']
print(df.tail(10))
