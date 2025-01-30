from aiogram.fsm.state import StatesGroup, State


class CreateOrder(StatesGroup):
    choose_type = State()
    choose_price = State()
    choose_start_date = State()
    choose_last_date = State()
    choose_place = State()
    appove_order = State()
