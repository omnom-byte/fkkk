python
import numpy as np
import talib

class Indicators:
    def __init__(self):
        pass

    def rsi(self, close_values, period):
        value = talib.RSI(close_values, timeperiod=period)[-1]
        return value

    def macd(self, close_values, period):
        macd, signal, hist = talib.MACD(close_values, fastperiod=12, slowperiod=26, signalperiod=9)
        return macd[-1], signal[-1]

    def bollinger_bands(self, close_values, period):
        upperband, middleband, lowerband = talib.BBANDS(close_values, timeperiod=period, nbdevup=2, nbdevdn=2)
        return upperband[-1], middleband[-1], lowerband[-1]
