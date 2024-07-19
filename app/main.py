import asyncio
import datetime

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core import config
from handlers import router as main_router
from tasks.get_currency_task import get_currency_rates

scheduler = AsyncIOScheduler()

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
task_scheduler = AsyncIOScheduler()
dp.include_router(main_router)


def schedule_jobs():
    # по желанию можно изменить час, когда таска будет выполняться. Для этого в hour указать час
    task_scheduler.add_job(get_currency_rates, "cron", hour=0)


async def main():
    schedule_jobs()
    task_scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
