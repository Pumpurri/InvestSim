import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradeSimulator.settings')

app = Celery('TradeSimulator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from stocks import fetch_stock_prices

    sender.add_periodic_task(
        crontab(hour=9, minute=0, day_of_week='1-5'),
        fetch_stock_prices.s(),
    )

    sender.add_periodic_task(
        crontab(minute='30,45,0,15', hour='9-16', day_of_week='1-5'),
        fetch_stock_prices.s(),
    )

    sender.add_periodic_task(
        crontab(hour=16, minute=30, day_of_week='1-5'),
        fetch_stock_prices.s(),
    )

