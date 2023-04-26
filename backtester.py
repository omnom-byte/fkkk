python
import pandas as pd
import talib
import numpy as np
import config

class Backtester:

    def __init__(self, df):
        self.df = df

    def run_backtest(self, rsi_period, macd_period, bb_period, overbought_rsi, oversold_rsi):
        buy_signals = []
        sell_signals = []
        traded_volume = []
        trades = []
        bought_at_price = 0
        bought_at = None

        for index, row in self.df.iterrows():
            if self.df['timestamp'][index] > (self.df['timestamp'][0] + pd.Timedelta(str(config.PERIOD) + ' minutes')):
                rsi = talib.RSI(self.df['close'][:index], rsi_period)[rsi_period-1:]
                macd, macd_signal, macd_hist = talib.MACD(self.df['close'][:index], fastperiod=macd_period[0], slowperiod=macd_period[1], signalperiod=macd_period[2])
                bb_upper, _, bb_lower = talib.BBANDS(self.df['close'][:index], timeperiod=bb_period)
                last_price = self.df['close'][index]
                last_vol = self.df['volume'][index]

                if rsi[-1] < oversold_rsi and macd[-1] > macd_signal[-1] and last_price <= bb_lower[-1]:
                    if bought_at_price == 0:
                        buy_signals.append(self.df['timestamp'][index])
                        traded_volume.append(last_price * config.USE_CURRENCY)
                        bought_at_price = last_price
                        bought_at = self.df['timestamp'][index]
                        trades.append(['BUY', last_vol, last_price, bought_at_price])
                elif bought_at_price != 0 and (rsi[-1] > overbought_rsi or macd[-1] < macd_signal[-1] or last_price >= bb_upper[-1]):
                    sell_signals.append(self.df['timestamp'][index])
                    profit = last_price / bought_at_price - 1
                    balance = traded_volume[-1] * (1 + profit)
                    trades.append(['SELL', last_vol, last_price, bought_at_price, bought_at, self.df['timestamp'][index], profit, balance])
                    bought_at_price = 0
                    bought_at = None

        return buy_signals, sell_signals, traded_volume, pd.DataFrame(trades, columns=['Action', 'Volume', 'Price', 'Bought_at_price', 'Bought_at', 'Sold_at', 'Profit', 'Balance'])
