import sys
import os
import django
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'self_storage'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
from storage.models import Order


def get_expired_orders():
    return Order.objects.filter(end_storage__lte=datetime.now().date())


def clean_db():
    expired_orders = get_expired_orders()
    if expired_orders.exists():
        expired_orders.update(cell__is_occupied=False)
        expired_orders.delete()


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_db, 'cron', hour=9)
    scheduler.start()
