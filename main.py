python
import time
from datetime import datetime, timedelta
import pytz
import talib
import numpy as np
import pandas as pd
from exchange import ExchangeAPI
import config
from indicators import Indicators
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Bot:
    def __init__(self):
        self.exchange = ExchangeAPI()
        self.indicators = Indicators()
        self.wallet = {'USD': 0, 'BTC': 0, 'ETH': 0, 'XRP': 0}
        self.interval = config.INTERVAL
        self.period = config.PERIOD
        self.backtest = config.BACKTEST_MODE
        if self.backtest:
            self.df = pd.read_csv('historical_data.csv', index_col=0)
            self.df.index = pd.to_datetime(self.df.index)
            self.df = self.df.iloc[::-1]
        else:
            self.df = pd.DataFrame()
        self.bot_start_time = time.time()

    def initialize(self):
        logging.info('Bot initializing...')
        self.bot_start_time = time.time()
        self.df = pd.DataFrame(columns=['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume',
                                        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                        'taker_buy_quote_asset_volume', 'ignore'])
        self.interval = config.INTERVAL
        self.period = config.PERIOD
        self.exchange = Exchange(config.API_KEY, config.API_SECRET)
        self.indicators = Indicators()
        self.wallet = self.get_wallet()
        self.google_sheets = GoogleSheetsAPI(config.GOOGLE_SHEETS_CREDS_FILE, config.SPREADSHEET_NAME)
        self.get_google_sheets_data()
        self.check_balance()
        self.backtest = config.BACKTEST_MODE

    def get_wallet(self):
        balance = self.exchange.client.futures_account_balance()
        wallet = {'USD': 0, 'BTC': 0, 'ETH': 0, 'XRP': 0}
        for item in balance:
            if item['asset'] == 'USDT':
                wallet['USD'] = float(item['balance'])
            elif item['asset'] == 'BTC':
                wallet['BTC'] = float(item['balance'])
            elif item['asset'] == 'ETH':
                wallet['ETH'] = float(item['balance'])
            elif item['asset'] == 'XRP':
                wallet['XRP'] = float(item['balance'])
        return wallet

    def check_balance(self):
        logging.info('Checking balance...')
        for currency in self.wallet:
            ticker_symbol = currency + config.USE_CURRENCY
            ticker_price = self.exchange.get_latest_price(ticker_symbol)
            if currency == 'USD':
                self.wallet[currency] = ticker_price * self.wallet[currency]
            else:
                asset_symbol = currency + config.USE_CURRENCY
                asset_balance = self.wallet[currency]
                asset_price = self.exchange.get_latest_price(asset_symbol)
                asset_value = asset_balance * asset_price
                self.wallet['USD'] += asset_value
        logging.info('Balance checked: USD: {}: BTC: {}; ETH: {}; XRP: {}'.format(
            self.wallet['USD'], self.wallet['BTC'], self.wallet['ETH'], self.wallet['XRP']))

    def get_google_sheets_data(self):
        logging.info('Reading data from Google Sheets...')
        worksheet = self.google_sheets.get_worksheet()
        data = worksheet.get_all_values()
        headers = data.pop(0)
        self.df = pd.DataFrame(data, columns=headers)
         def update_google_spreadsheet(self, symbol, action, price, quantity, fee):
        logging.info('Updating Google Sheets...')
        self.df = self.df.append({
            'timestamp': datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol,
            'action': action,
            'price': price,
            'quantity': quantity,
            'fee': fee,
            'balance': self.wallet['USD']
        }, ignore_index=True)
        worksheet = self.google_sheets.get_worksheet()
        worksheet.insert_row(self.df.iloc[-1].values.tolist())
        logging.info('Google Sheets updated')

    def backtest(self):
        # to be implemented
        pass

    def run(self):
        logging.info('Bot started at {}'.format(datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')))
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.bot_start_time
            if elapsed_time > config.LOG_INTERVAL * 3600:
                self.bot_start_time = current_time
                logging.info('Bot is still running at {}'.format(datetime.now(pytz.timezone(config.TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')))
            try:
                candles = self.exchange.get_candles(symbol='BTCUSDT', interval=self.interval)
            except Exception as e:
                logging.error(str(e))
                time.sleep(30)
                continue
            self.df = pd.concat([self.df, pd.DataFrame(candles)])
            self.df = self.df.drop_duplicates(subset=['timestamp'], keep='first')
            self.df = self.df.sort_values(by='timestamp')
            self.check_balance()
            if self.backtest:
                backtest_res = self.backtest()
            for symbol in config.PAIRS:
                try:
                    symbol_df = self.df[self.df['symbol'] == symbol]
                    if self.backtest:
                        latest_price = symbol_df.iloc[-1]['close']
                    else:
                        latest_price = self.exchange.get_latest_price(symbol)
                except Exception as e:
                    logging.error('Error with symbol {}: '.format(symbol) + str(e))
                    continue
                    
           if len(symbol_df) > self.period:
    rsi_value = self.indicators.rsi(symbol_df['close'].values, self.period)
    macd_value, macd_signal = self.indicators.macd(symbol_df['close'].values, self.period)
    bb_bands = self.indicators.bollinger_bands(symbol_df['close'].values, self.period)
    bb_upper, bb_middle, bb_lower = bb_bands[0][-1], bb_bands[1][-1], bb_bands[2][-1]
    if rsi_value >= config.RSI_OVERBOUGHT and macd_value < macd_signal and latest_price <= bb_lower:
        self.place_order(symbol, 'BUY', latest_price)
    elif rsi_value <= config.RSI_OVERSOLD and macd_value > macd_signal and latest_price >= bb_upper:
        self.place_order(symbol, 'SELL', latest_price)

        self.update_google_spreadsheet(symbol=symbol, action='BUY', price=latest_price, quantity=available_amount, fee=0, balance=self.wallet[config.USE_CURRENCY])
        logging.info('{} BUY order for {} {} placed at {}.'.format(symbol, available_amount, symbol.split(config.USE_CURRENCY)[0], latest_price))
    elif rsi_value >= config.RSI_OVERBOUGHT and macd_value > macd_signal:
        self.place_order(symbol, 'SELL', latest_price)

        self.update_google_spreadsheet(symbol=symbol, action='SELL', price=latest_price, quantity=available_amount, fee=0, balance=self.wallet[config.USE_CURRENCY])
        logging.info('{} SELL order for {} {} placed at {}.'.format(symbol, available_amount, symbol.split(config.USE_CURRENCY)[0], latest_price))
    elif rsi_value <= config.RSI_OVERSOLD and macd_value < macd_signal:
        current_qty = self.get_balances(symbol)

        self.place_order(symbol, 'BUY', latest_price)

        self.update_google_spreadsheet(symbol=symbol, action='BUY', price=latest_price, quantity=quantity, fee=0, balance=self.wallet[config.USE_CURRENCY])
        logging.info('{} BUY order for {} {} placed at {}.'.format(symbol, quantity, symbol.split(config.USE_CURRENCY)[0], latest_price))
    else:
        pass    
