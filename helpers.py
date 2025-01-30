import sys
import os
import django
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'self_storage'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
from storage.models import Cell, CellTariff, Client, Order, Warehouse


@sync_to_async
def get_cell_types():
    return list(CellTariff.objects.all())


@sync_to_async
def get_warehouses():
    return list(Warehouse.objects.all())


@sync_to_async
def get_cell_price_by_id(id):
    return CellTariff.objects.filter(id=id).first().price_per_day


@sync_to_async(thread_sensitive=False)
def get_orders_expiring_month():
    deadline = datetime.now().date() + timedelta(days=30)
    return list(Order.objects.filter(end_storage=deadline).values("client__tg_id", "end_storage"))


@sync_to_async(thread_sensitive=False)
def get_orders_expiring_two_weeks():
    deadline = datetime.now().date() + timedelta(weeks=2)
    return list(Order.objects.filter(end_storage=deadline).values("client__tg_id", "end_storage"))


@sync_to_async(thread_sensitive=False)
def get_orders_expiring_week():
    deadline = datetime.now().date() + timedelta(weeks=1)
    return list(Order.objects.filter(end_storage=deadline).values("client__tg_id", "end_storage"))


@sync_to_async(thread_sensitive=False)
def get_orders_expiring_three_days():
    deadline = datetime.now().date() + timedelta(days=3)
    return list(Order.objects.filter(end_storage=deadline).values("client__tg_id", "end_storage"))


async def get_all_orders_expiring():
    expiring_month = await get_orders_expiring_month()
    expiring_two_weeks = await get_orders_expiring_two_weeks()
    expiring_week = await get_orders_expiring_week()
    expiring_three_days = await get_orders_expiring_three_days()

    all_expiring_orders = (expiring_month
                           + expiring_two_weeks
                           + expiring_week
                           + expiring_three_days)
    return all_expiring_orders


@sync_to_async(thread_sensitive=False)
def get_orders_expiring():
    deadline = datetime.now() + timedelta(days=1)
    return list(Order.objects.filter(end_storage=deadline.date()).values("client__tg_id", "end_storage"))


@sync_to_async
def create_order(state_data, tg_id):
    client = Client.objects.filter(tg_id=tg_id).first()
    if not client:
        print(f"❌ Ошибка: Клиент с tg_id={tg_id} не найден!")
        return False

    if "isCurier" not in state_data:
        warehouse = Warehouse.objects.filter(id=state_data['place']).first()
        cell_tariff = CellTariff.objects.filter(price_per_day=state_data['price']).first()

        # Получаем первую свободную ячейку
        cell = Cell.objects.filter(
            is_occupied=False,
            cell_size=cell_tariff,
            address=warehouse
        ).first()
        # Получаем одну запись тарифа
        cell_tariff = CellTariff.objects.filter(price_per_day=state_data['price']).first()
        
        # Получаем первую свободную ячейку
        cell = Cell.objects.filter(is_occupied=False, cell_size=cell_tariff).first()

        if cell:  # Проверяем, что cell найден
            date_first = datetime(
                year=state_data['year_first'],
                month=state_data['month_first'],
                day=state_data['day_first']
            )
            date_last = datetime(
                year=state_data['year_last'],
                month=state_data['month_last'],
                day=state_data['day_last']
            )

            # Создаём заказ
            order = Order.objects.create(
                client=client,
                start_storage=date_first,
                end_storage=date_last,
                cell=cell
            )

            # Обновляем статус ячейки
            order.cell.is_occupied = True
            order.cell.save()
        else:
            return False
    else:
        # Получаем одну запись тарифа
        cell_tariff = CellTariff.objects.filter(price_per_day=state_data['price']).first()
        
        # Получаем первую свободную ячейку
        cell = Cell.objects.filter(is_occupied=False, cell_size=cell_tariff).first()

        if cell:  # Проверяем, что cell найден
            date_first = datetime(
                year=state_data['year_first'],
                month=state_data['month_first'],
                day=state_data['day_first']
            )
            date_last = datetime(
                year=state_data['year_last'],
                month=state_data['month_last'],
                day=state_data['day_last']
            )

            # Создаём заказ
            order = Order.objects.create(
                client=client,
                contacts=state_data['contact'],
                start_storage=date_first,
                end_storage=date_last,
                cell=cell
            )

            # Обновляем статус ячейки
            order.cell.is_occupied = True
            order.cell.save()
        else:
            return False
    return True


@sync_to_async
def get_chat_id(tg_id, name):
    user = Client.objects.filter(tg_id=tg_id).first()
    if user:
        pass
    else:
        Client.objects.create(tg_id=tg_id, client_name=name)
