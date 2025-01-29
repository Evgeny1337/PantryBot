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


@sync_to_async
def get_orders_expiring_month():
    deadline = datetime.now() + timedelta(days=30)
    return list(Order.objects.filter(end_storage__date=deadline.date()))


@sync_to_async
def get_orders_expiring_two_weeks():
    deadline = datetime.now() + timedelta(weeks=2)
    return list(Order.objects.filter(end_storage__date=deadline.date()))


@sync_to_async
def get_orders_expiring_week():
    deadline = datetime.now() + timedelta(weeks=1)
    return list(Order.objects.filter(end_storage__date=deadline.date()))


@sync_to_async
def get_orders_expiring_three_days():
    deadline = datetime.now() + timedelta(days=3)
    return list(Order.objects.filter(end_storage__date=deadline.date()))


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
