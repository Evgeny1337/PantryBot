import random
from datetime import timedelta
from django.db import IntegrityError
from faker import Faker
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
from storage.models import Cell, CellTariff, Client, Order


def generate_random_tg_id():
    while True:
        # Генерируем случайное число длиной 9 цифр
        tg_id = random.randint(10**8, 10**9 - 1)
        try:
            Client.objects.get(tg_id=tg_id)
        except Client.DoesNotExist:
            return tg_id
        else:
            continue  # Если такой tg_id уже существует, продолжаем цикл


def main():
    fake = Faker('ru_RU')

    for _ in range(25):
        tg_id = generate_random_tg_id()
        client = Client(tg_id=tg_id, client_name=fake.name())
        try:
            client.save()
        except IntegrityError as e:
            print(f"Ошибка при сохранении клиента: {e}")

    for _ in range(5):
        cell_tariff = CellTariff.objects.order_by('?').first()
        cell = Cell(cell_size=cell_tariff, is_occupied=False)
        cell.save()

    clients = list(Client.objects.all())[:5]
    cells = list(Cell.objects.all())[:5]

    for i in range(5):
        order = Order(
            client=clients[i],
            contacts=fake.phone_number(),
            start_storage=fake.date_time_this_year(),
            end_storage=fake.future_datetime(),
            address=fake.address(),
            cell=cells[i]
        )
        order.save()

    print("Случайные данные сгенерированы.")


if __name__ == "__main__":
    main()