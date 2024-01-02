import ccxt
import pandas as pd
import numpy as np

# Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your Binance API key and secret
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Define trading pairs and their parameters
trading_pairs = [
    {'symbol': 'ADABTC', 'base': 'ADA', 'quote': 'BTC', 'quantity': 10, 'short_window': 20, 'long_window': 50},
    {'symbol': 'ETHBTC', 'base': 'ETH', 'quote': 'BTC', 'quantity': 0.1, 'short_window': 15, 'long_window': 40},
    # Add more trading pairs as needed
]

# Initialize the Binance exchange connection
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Fetch historical data
def fetch_historical_data(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['Short_MA'] = data['close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['close'].rolling(window=long_window).mean()

# Trading strategy based on moving averages
def implement_strategy(data):
    data['Signal'] = 0  # 0 indicates no signal
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()

# Execute trades
def execute_trades(data, symbol, quantity):
    for i in range(len(data) - 1):
        if data['Position'].iloc[i] == 1:
            print(f'Buy {symbol}: {data.index[i + 1]}')
            # Place buy order here using your trading platform API
            exchange.create_market_buy_order(symbol, quantity)
        elif data['Position'].iloc[i] == -1:
            print(f'Sell {symbol}: {data.index[i + 1]}')
            # Place sell order here using your trading platform API
            exchange.create_market_sell_order(symbol, quantity)

# Main function
def main():
    for pair in trading_pairs:
        symbol = pair['symbol']
        quantity = pair['quantity']
        short_window = pair['short_window']
        long_window = pair['long_window']

        # Fetch historical data
        historical_data = fetch_historical_data(symbol, '1h', limit=200)

        # Calculate moving averages
        calculate_moving_averages(historical_data, short_window, long_window)

        # Implement trading strategy
        implement_strategy(historical_data)

        # Execute trades
        execute_trades(historical_data, symbol, quantity)

if __name__ == '__main__':
    main()
