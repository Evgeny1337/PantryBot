import sys
import os
import django
import requests
import time
from urllib.parse import urlparse
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'self_storage'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
from storage.models import Order, ClickCounter, Cell


def get_expired_orders():
    return Order.objects.filter(end_storage__lte=datetime.now().date())


def clean_db():
    expired_orders = get_expired_orders()
    if expired_orders.exists():
        Cell.objects.filter(id__in=expired_orders.values_list('cell_id', flat=True)).update(is_occupied=False)
        expired_orders.delete()
        print("все устаревшие записи удалены")


def update_clicks():
    link = urlparse('https://vk.cc/cI2xjl')
    counter = ClickCounter.objects.first()
    load_dotenv()
    token = os.getenv("VK_SERVICE_ACCESS_KEY")
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link.path.replace('/', ''),
        'interval': 'forever'
    }
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats',
                            params=params)
    response.raise_for_status()
    api_response = response.json()
    if 'error' in api_response:
        return
    views = int(api_response['response']['stats'][0]['views'])
    counter.clicks = views
    counter.save()
    print(int(api_response['response']['stats'][0]['views']))


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_db, 'interval', minutes=1)
    scheduler.add_job(update_clicks, 'interval', minutes=1)
    scheduler.start()

    try:
        while True:
            time.sleep(60)  # Ожидание 1 минуту перед следующей проверкой
    except KeyboardInterrupt:
        scheduler.shutdown()
