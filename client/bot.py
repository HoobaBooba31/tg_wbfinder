from aiogram import Bot
from aiogram import Dispatcher
import main_dialogue
from dotenv import load_dotenv
import os
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio


async def start_bot():
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_dialogue.ls_router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(start_bot())
