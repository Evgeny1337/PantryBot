from aiogram import types
from keyboard import create_order_keyboard, choose_type_keyboard, approve_order
from aiogram.fsm.context import FSMContext
from state import CreateOrder
from helpers import get_chat_id
import datetime

async def start_handler(message:types.Message,state:FSMContext):
    await get_chat_id(message.from_user.id, message.from_user.full_name)
    await state.clear()
    text = """Добро пожаловать в наш бот аренды складских помещений!

Мы поможем вам быстро и удобно арендовать место для хранения вещей на любой срок.

📌 Что умеет этот бот?
🔹 Аренда склада — выберите нужный размер ячейки и срок хранения.
🔹 Гибкие условия — арендуйте место на дни, недели или месяцы.
🔹 Уведомления — бот напомнит вам о сроке окончания хранения.
🚀 Начните прямо сейчас — нажмите «Создать заказ»!

С правилами хранения вы можете ознакомиться по ссылке:
https://docs.google.com/document/d/1TSUO4U56FNMGfAysA5fqNY6ZsRPj14lRqEP955W1-YA/edit?usp=sharing

Продолжая, вы соглашаетесь с обработкой персональных данных:
https://docs.google.com/document/d/1wy-ziowpBP8PFV6AIu893FKTDr4o6Hv7bBnBrTz6Mrk/edit?usp=sharing"""
    await message.answer(text, reply_markup=create_order_keyboard())


async def create_order(message:types.Message,state:FSMContext):
    await message.delete()
    await state.set_state(CreateOrder.choose_type)
    await message.answer(text="Выберите спопсоб создания заказа",reply_markup=choose_type_keyboard())


async def fill_contact(message:types.Message,state:FSMContext):
    await message.delete()
    await state.set_state(CreateOrder.appove_order)
    state_data = await state.get_data()
    date_first = datetime.datetime(year=state_data['year_first'],
                                   month=state_data['month_first'],
                                   day=state_data['day_first'])
    date_last = datetime.datetime(year=state_data['year_last'],
                                  month=state_data['month_last'],
                                  day=state_data['day_last'])
    day_count = (date_last - date_first).days
    result_data = (
        f"Дата начала хранения: {state_data['year_first']}.{state_data['month_first']}.{state_data['day_first']}\n"
        f"Дата конца хранения: {state_data['year_last']}.{state_data['month_last']}.{'day_last'}\n"
        f"Общая сумма: {state_data['price'] * day_count} р.\n"
        f"Контактные данные: {message.text}"
    )
    await state.update_data({'contact': message.text})
    await message.answer("Завершите оформление\nДанные заказа:\n" + result_data,reply_markup=approve_order())
