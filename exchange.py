import os

import ccxt

from config import EXCHANGE_API_SECRET, EXCHANGE_API_KEY

class Exchange:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': EXCHANGE_API_KEY,
            'secret': EXCHANGE_API_SECRET
        })

    def get_exchange_caps(self) -> dict:
        caps = self.exchange.load_markets()
        return caps

    def get_exchange_symbol(self, symbol: str, caps: list) -> str:
        symbols = [s for s in caps.keys() if symbol in s]
        return symbols[0]

    def get_exchange_candles(self, symbol: str, period_weight: float) -> List[float]:
        timeframe = self.get_timeframe(period_weight)
        candles = self.exchange.fetch_ohlcv(symbol, timeframe)
        candles = [c[4] for c in candles]
        return candles
    
    def limit_buy_order(self, symbol: str, buy_price: float, amount: float) -> None:
        order = self.exchange.create_limit_buy_order(symbol, amount, buy_price)

    def limit_sell_order(self, symbol: str, sell_price: float, amount: float) -> None:
        order = self.exchange.create_limit_sell_order(symbol, amount, sell_price)

    def get_timeframe(self, period_weight: float) -> str:
        timeframe = '5m'
        if period_weight > 0.11:
            timeframe = '15m'
        if period_weight > 0.27:
            timeframe = '1h'
        if period_weight > 0.83:
            timeframe = '4h'

        return timeframe
