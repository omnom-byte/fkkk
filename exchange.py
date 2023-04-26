python
from binance.client import Client
import config

class ExchangeAPI:

    def __init__(self):
        self.client = Client(config.API_KEY, config.API_SECRET)

    def get_latest_price(self, symbol):
        ticker = self.client.get_ticker(symbol=symbol)
        return float(ticker['lastPrice'])

    def get_candles(self, symbol, interval):
        return self.client.get_klines(symbol=symbol, interval=interval)

    def place_order(self, symbol, side, quantity, price):
        self.client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price)
