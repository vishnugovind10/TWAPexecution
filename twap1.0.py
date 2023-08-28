import time
from binance.client import Client

# Replace with your Binance API key and secret
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def get_average_price(symbol):
    ticker = client.get_ticker(symbol=symbol)
    return float(ticker['lastPrice'])

def execute_market_order(symbol, quantity):
    order = client.create_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )
    return order

def twap_algorithm(symbol, target_quantity, interval_minutes):
    total_quantity = target_quantity
    interval_seconds = interval_minutes * 60

    while total_quantity > 0:
        interval_quantity = total_quantity / (target_quantity // interval_seconds)
        average_price = get_average_price(symbol)
        print(f"Executing order for {interval_quantity:.8f} {symbol} at average price {average_price:.8f}")
        
        execute_market_order(symbol, interval_quantity)
        
        total_quantity -= interval_quantity
        time.sleep(interval_seconds)

def main():
    symbol = 'BTCUSDT'  # Replace with your desired trading pair
    target_quantity = 0.01  # Replace with your desired order quantity
    interval_minutes = 5  # Replace with your desired interval in minutes

    twap_algorithm(symbol, target_quantity, interval_minutes)

if __name__ == '__main__':
    main()
