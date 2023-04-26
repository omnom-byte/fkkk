from typing import List
import asyncio
import time

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from exchange import Exchange
from indicators import Indicators
from config import PERIODS, PERIOD_WEIGHTS, TRADE_AMOUNT, TRADE_SYMBOL

class TradingBot:
    def __init__(self):
        self.exchange = Exchange()

    async def trading(self, period_weight: float, pipe: asyncio.Queue) -> None:
        indicators = Indicators(period_weight, PERIODS)

        while True:
            caps = self.exchange.get_exchange_caps()
            symbol = self.exchange.get_exchange_symbol(TRADE_SYMBOL, caps)
            candles = self.exchange.get_exchange_candles(symbol, period_weight)
            if not candles:
                time.sleep(1)
                continue
            diff = round(candles[-1] - candles[-2], 2)

            indicators.add_price(candles[-1])

            if indicators.is_sell_signal():
                sell_price = candles[-1] - diff
                self.exchange.limit_sell_order(TRADE_SYMBOL, sell_price, TRADE_AMOUNT)
                await pipe.put("Продано")
            elif indicators.is_buy_signal():
                buy_price = candles[-1] + diff
                self.exchange.limit_buy_order(TRADE_SYMBOL, buy_price, TRADE_AMOUNT)
                await pipe.put("Куплено")

            await asyncio.sleep(10)
