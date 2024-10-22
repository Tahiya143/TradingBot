import pandas as pd
import numpy as np
import requests
import time

# API Credentials
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://paper-api.alpaca.markets'  # Change to live API for real trading

# Function to fetch historical data
def fetch_historical_data(symbol, timeframe='1D', limit=100):
    url = f"{BASE_URL}/v2/stocks/{symbol}/bars?timeframe={timeframe}&limit={limit}"
    headers = {'APCA_API_KEY_ID': API_KEY, 'APCA_API_SECRET_KEY': API_SECRET}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to execute trades
def place_order(symbol, qty, side, order_type='market'):
    url = f"{BASE_URL}/v2/orders"
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': order_type,
        'time_in_force': 'gtc'
    }
    headers = {'APCA_API_KEY_ID': API_KEY, 'APCA_API_SECRET_KEY': API_SECRET}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Simple Moving Average Strategy
def trading_strategy(symbol):
    data = fetch_historical_data(symbol)
    prices = [bar['close'] for bar in data['bars']]
    df = pd.DataFrame(prices, columns=['Close'])

    # Calculate indicators
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    # Check for buy/sell signals
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:  # Buy signal
        place_order(symbol, qty=1, side='buy')
        print(f"Buying {symbol}")

    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:  # Sell signal
        place_order(symbol, qty=1, side='sell')
        print(f"Selling {symbol}")

# Main loop
def main():
    symbol = 'AAPL'  # Example stock symbol
    while True:
        trading_strategy(symbol)
        time.sleep(60 * 5)  # Run every 5 minutes

if __name__ == "__main__":
    main()
