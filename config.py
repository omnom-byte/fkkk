API_KEY = 'YOUR_API_KEY_HERE'
API_SECRET = 'YOUR_API_SECRET_KEY_HERE'
INTERVAL = '15m'
PAIRS = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']
USE_CURRENCY = 'USDT'
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MIN_TRADE_VOLUME = 10
MIN_TRADE_RATE = 0.01
LESS_THAN_MIN_TRADE_VOLUME = -1
BUY_PERCENTAGE = 0.01
SELL_PERCENTAGE = 0.01
PORTFOLIO = {'BTC': 0, 'ETH': 0, 'XRP': 0}
GOOGLE_SHEETS_CREDS_FILE = 'creds.json'
SPREADSHEET_NAME = 'Trading Log'
GOOGLE_SHEETS_COLUMNS = {
    'timestamp': 'A',
    'symbol': 'B',
    'action': 'C',
    'price': 'D',
    'quantity': 'E',
    'fee': 'F',
    'balance': 'G'
}
PERIOD = 14
LOG_INTERVAL = 24
BACKTEST_MODE = False