import unittest

from exchange import Exchange
from backtester import Backtester

exchange = Exchange()

class TestExchange(unittest.TestCase):
    def test_get_exchange_caps(self):
        caps = exchange.get_exchange_caps()
        self.assertTrue(isinstance(caps, dict))

    def test_get_exchange_candles(self):
        symbol = 'BTC/USDT'
        period_weight = 0.1
        candles = exchange.get_exchange_candles(symbol, period_weight)
        self.assertTrue(isinstance(candles, list))

class TestBacktester(unittest.TestCase):
    def test_get_trade_history(self):
        start_time = 1625000000
        end_time = 1625082000
        period_weight = 0.3
        backtester = Backtester(exchange)
        trade_history = backtester.get_trade_history(start_time, end_time, period_weight)
        self.assertTrue(isinstance(trade_history, list))
