from typing import List
import talib
from config import LENGTH, OFFSET

class Indicators:
    def __init__(self, period_weight: float, periods: List[int]):
        self.period_weight = period_weight
        self.periods = [int(p * period_weight) for p in periods]
        self.window_size = max(self.periods) + OFFSET
        self.prices = []

    def is_buy_signal(self) -> bool:
        _, _, macd_hist = talib.MACDFIX(self.prices, signalperiod=self.periods[0], fastperiod=self.periods[1], slowperiod=self.periods[2])
        if macd_hist[-1] <= macd_hist[-2] and macd_hist[-2] <= macd_hist[-3] and macd_hist[-3] <= macd_hist[-4] and macd_hist[-4] <= macd_hist[-5]:
            return True
        return False

    def is_sell_signal(self) -> bool:
        _, _, macd_hist = talib.MACDFIX(self.prices, signalperiod=self.periods[0], fastperiod=self.periods[1], slowperiod=self.periods[2])
        if macd_hist[-1] >= macd_hist[-2] and macd_hist[-2] >= macd_hist[-3] and macd_hist[-3] >= macd_hist[-4] and macd_hist[-4] >= macd_hist[-5]:
            return True
        return False

    def add_price(self, price: float) -> None:
        if len(self.prices) == self.window_size:
            self.prices.pop(0)
        self.prices.append(price)
