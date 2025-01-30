from aiogram import types
from datetime import datetime
import calendar
from helpers import get_cell_types, get_warehouses


def create_order_keyboard():
    keyboard_buttons = [[types.KeyboardButton(text="Создать заказ")]]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons)


def choose_type_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text='Услуга курьера',callback_data='choose_type_deliver')],
                        [types.InlineKeyboardButton(text='Доаставка в пункт самовывоза',callback_data='choose_type_place')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_type_cell():
    keyboard_buttons = []
    cell_types = await get_cell_types()
    for cell_type in cell_types:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cell_type.size}, {cell_type.price_per_day} р. в день',
            callback_data=f'choose_cell_{cell_type.id}')])
    keyboard_buttons.append([types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_type_place():
    keyboard_buttons = []
    places = await get_warehouses()
    for warehouse in places:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{warehouse.name}, {warehouse.adress}',
            callback_data=f'choose_place_{warehouse.id}')])
    keyboard_buttons.append([types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def approve_order():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Подтвердить заказ",callback_data='approve')],
                        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def create_calendar(year, month, type_callback):
    keyboard_buttons = [[types.InlineKeyboardButton(
        text='<<', callback_data=f'month_prev_{year}_{month}'),
        types.InlineKeyboardButton(
            text="{} - {}".format(calendar.month_name[month],year), callback_data='ignore'),
        types.InlineKeyboardButton(
            text='>>', callback_data=f'month_next_{year}_{month}')],]

    month_days = calendar.monthcalendar(year, month)
    print("test",year, month)
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(
                    text=' ', callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(day),
                           callback_data=f'{type_callback}_day_{year}_{month}_{day}'))
        keyboard_buttons += [row]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def exit_button():
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]])
