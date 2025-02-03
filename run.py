from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
import asyncio
import logging
import sys
from aiogram.client.session.aiohttp import AiohttpSession
from handlers import router as client_router
from admin_handlers import router as admin_router

from database.models import async_main
from config import TOKEN


async def main(dp: Dispatcher, token: str):
    await async_main()  # Ma'lumotlar bazasi bilan ishlash
    session = AiohttpSession()  # Bot uchun HTTP sessiya
    
    bot = Bot(token=token, session=session)  # Bot instance
    dp.include_router(client_router)  # Bosh routerni ulaymiz
    dp.include_router(admin_router)  # Admin routerni ulaymiz

    await dp.start_polling(bot)  # Bot pollingni boshlaydi

# Main blok
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)  # Loglar
    try:
        dp = Dispatcher()  # Dispatcher yaratiladi
        asyncio.run(main(dp, TOKEN))  # Asosiy funksiya chaqiriladi
    except KeyboardInterrupt:
        print('Exit')  # Keyboard interruput qilinganda chiqadi