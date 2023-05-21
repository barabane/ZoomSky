import asyncio
from bot_settings import bot, dp
from handlers.main_handler import router as main_router


async def main():
    dp.include_routers(main_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
