import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from exchange import Exchange
from config import API_TOKEN
from smartsheet_api import SheetAPI
from rading_bot import TradingBot
from utils import get_logger

logging.basicConfig(level=logging.INFO)
log = get_logger()

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

exchange = Exchange()
trading_bot = TradingBot()
sheet_api = SheetAPI()
