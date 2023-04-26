import asyncio

from bot import dp, bot
from config import API_TOKEN

if __name__ == '__main__':
    from handlers import *

    loop = asyncio.get_event_loop()
    try:
        executor = asyncio.ensure_future(dp.start_polling())
        loop.run_until_complete(executor)
    finally:
        loop.close()
