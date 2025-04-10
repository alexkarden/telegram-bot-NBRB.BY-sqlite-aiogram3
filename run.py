import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN, CHECKINTERVAL,SHORTLISTOFCURRENCY
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import router
from script import init_db, add_db, rassilka


bot = Bot(token=TOKEN)
dp = Dispatcher()



async def main():
    await init_db()
    await add_db()
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(add_db, trigger='interval', minutes=CHECKINTERVAL)
    scheduler.add_job(
        rassilka,
        trigger=CronTrigger(hour=10, minute=00),
        kwargs={
            'bot': bot,
            'currency_list': SHORTLISTOFCURRENCY,
            'status': 'thrice'
        }
    )
    scheduler.add_job(
        rassilka,
        trigger=CronTrigger(hour=12, minute=30),
        kwargs={
            'bot': bot,
            'currency_list': SHORTLISTOFCURRENCY,
            'status': 'thrice'
        }
    )
    scheduler.add_job(
        rassilka,
        trigger=CronTrigger(hour=14, minute=30),
        kwargs={
            'bot': bot,
            'currency_list': SHORTLISTOFCURRENCY,
            'status': 'daily'
        }
    )
    scheduler.add_job(
        rassilka,
        trigger=CronTrigger(hour=15, minute=00),
        kwargs={
            'bot': bot,
            'currency_list': SHORTLISTOFCURRENCY,
            'status': 'thrice'
        }
    )





    scheduler.start()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')