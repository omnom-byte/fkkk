from typing import List
import time

from exchange import Exchange
from indicators import Indicators
from config import PERIOD_WEIGHTS, TRADE_SYMBOL

class Backtester:
    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    def get_trade_history(self, test_start_time: float, test_end_time: float, period_weight: float) -> List:
        trade_history = []
        indicators = Indicators(period_weight, PERIODS)

        caps = self.exchange.get_exchange_caps()
        symbol = self.exchange.get_exchange_symbol(TRADE_SYMBOL, caps)
        candles = self.exchange.get_exchange_candles(symbol, period_weight)

        for i in range(int(test_start_time), int(test_end_time)):
            if time.time() - i > 0:
                break

            indicators.add_price(candles[i])
            if indicators.is_buy_signal():
                buy_price = candles[i]
                self.exchange.limit_buy_order(TRADE_SYMBOL, buy_price, TRADE_AMOUNT)
                trade_history.append(f'Покупка: {candles[i]}, {time.ctime(i)}')
            elif indicators.is_sell_signal():
                sell_price = candles[i]
                self.exchange.limit_sell_order(TRADE_SYMBOL, sell_price, TRADE_AMOUNT)
                trade_history.append(f'Продажа: {candles[i]}, {time.ctime(i)}')

        return trade_history
