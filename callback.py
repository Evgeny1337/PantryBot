from aiogram import types
from aiogram.fsm.context import FSMContext
from state import CreateOrder
from keyboard import choose_type_cell, create_calendar, choose_type_place
from helpers import get_cell_price_by_id
import datetime


async def choose_type_callback(callback:types.CallbackQuery,state:FSMContext):
    data = callback.data.split("_")[2]
    await callback.message.delete()
    if data == 'deliver':
        await state.update_data({"place":"courier","price":0,"place":0})
        await callback.message.answer(text="Введите контактные данные")
    if data == 'place':
        await state.set_state(CreateOrder.choose_price)
        murkup = await choose_type_cell()
        await callback.message.answer("Выберите размер ячейки",reply_markup=murkup)


async def choose_price_callback(callback:types.CallbackQuery,state:FSMContext):
    data = callback.data.split("_")[2]
    # Если из бдшки то генерировать условие
    await state.set_state(CreateOrder.choose_start_date)
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.update_data({"year_first":current_year,"month_first":current_month})
    await callback.message.delete()
    price = await get_cell_price_by_id(data) 
    await state.update_data({"price": price}) # не знаю, какую цену надо сохранять сюда, но сохраняется цена в день за ячейку
    await callback.message.answer(text='Выберите какого числа вы привезете свои вещи', reply_markup=create_calendar(current_year,current_month,'first'))


async def swith_month_callback(callback:types.CallbackQuery,state:FSMContext):
    data = callback.data.split("_")[1]
    state_data = await state.get_data()
    if 'year_last' not in state_data:
        current_year = state_data['year_first']
        current_month = state_data['month_first']
    else:
        current_year = state_data['year_last']
        current_month = state_data['month_last']

    if data == 'prev':
        if current_month - 1 <= 0:
            current_year -= 1
            current_month = 12
        else:
            current_month -= 1
    if data == 'next':
        if current_month + 1 > 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1
    if 'year_last' not in state_data:
        await state.update_data({'year_first':current_year,'month_first':current_month})
        await callback.message.edit_text(text='Выберите какого числа вы привезете свои вещи',reply_markup=create_calendar(current_year,current_month,'first'))
    else:
        await state.update_data({'year_last':current_year,'month_last':current_month})
        await callback.message.edit_text(text='Выберите какого числа вы привезете свои вещи',reply_markup=create_calendar(current_year,current_month,'second'))


async def choose_first_date_callback(callback:types.CallbackQuery,state:FSMContext):
    data = int(callback.data.split("_")[4])
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.update_data({"day_first":data, 'year_last':current_year,'month_last':current_month})
    await state.set_state(CreateOrder.choose_last_date)
    await callback.message.delete()
    await callback.message.answer(text="Выберите какого числа вы хотите забрать заказ", reply_markup=create_calendar(current_year,current_month,'second'))


async def choose_last_date_callback(callback:types.CallbackQuery,state:FSMContext):
    data = int(callback.data.split("_")[4])
    await state.update_data({"day_last":data})
    await state.set_state(CreateOrder.choose_place)
    await callback.message.delete()
    markup = await choose_type_place()
    await callback.message.answer(text="Выберите пункт примеа",reply_markup=markup)


async def drop_state_callback(callback:types.CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text="Вы отменили заполнение отказа")
