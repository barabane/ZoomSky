import os
from dotenv import load_dotenv
from tzlocal import get_localzone
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
scheduler = AsyncIOScheduler(timezone=get_localzone())

bot = Bot(os.environ.get('BOT_TOKEN'))
dp = Dispatcher()
