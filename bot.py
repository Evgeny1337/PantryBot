import asyncio
import logging
import sys
from os import environ
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from handler import start_handler, create_order, fill_contact
from callback import choose_type_callback,choose_price_callback,drop_state_callback,swith_month_callback,choose_first_date_callback,choose_last_date_callback,choose_place_callback,approve_callback
from state import CreateOrder
from aiogram import F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from helpers import get_all_orders_expiring, get_orders_expiring

load_dotenv()
TOKEN = environ['BOT_TOKEN']
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_notification_qwe():  # для тестов
    orders = await get_orders_expiring()
    for order in orders:
        try:
            await bot.send_message(chat_id=order["client__tg_id"],
                                   text=f'''Приветсвуем!\nНапоминаем, что сроки хранения подходят к концу.
Вещи со склада вы можете забрать до {order["end_storage"].strftime("%d.%m.%Y")}''')
        except Exception:
            print('Пользователь запретил отправлять ему сообщения')


async def send_notification():
    orders = await get_all_orders_expiring()
    for order in orders:
        try:
            await bot.send_message(
                chat_id=order["client__tg_id"],
                text=f'''Приветствуем!\nНапоминаем, что сроки хранения подходят к концу.
Вещи со склада вы можете забрать до {order["end_storage"].strftime("%d.%m.%Y")}'''
            )
        except Exception:
            print('Пользователь запретил отправлять ему сообщения')


async def main() -> None:
    dp = Dispatcher()
    dp.message.register(start_handler,CommandStart())
    dp.message.register(create_order,F.text=="Создать заказ")
    dp.message.register(fill_contact, F.text, CreateOrder.fill_contact)
    dp.callback_query.register(drop_state_callback,F.data == 'exit')
    dp.callback_query.register(swith_month_callback,F.data.startswith('month_'))
    dp.callback_query.register(choose_type_callback,F.data.startswith('choose_type_'),CreateOrder.choose_type)
    dp.callback_query.register(choose_price_callback,F.data.startswith('choose_cell_'),CreateOrder.choose_price)
    dp.callback_query.register(choose_first_date_callback,F.data.startswith('first_'),CreateOrder.choose_start_date)
    dp.callback_query.register(choose_last_date_callback,F.data.startswith('second_'),CreateOrder.choose_last_date)
    dp.callback_query.register(choose_place_callback,F.data.startswith('choose_place_'),CreateOrder.choose_place)
    dp.callback_query.register(approve_callback,F.data.startswith('approve'),CreateOrder.appove_order)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notification, 'cron', hour=9)
    scheduler.add_job(send_notification_qwe, 'interval', minutes=1)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
