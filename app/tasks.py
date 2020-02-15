from app import celery
from celery.schedules import crontab




@celery.task()
def add_together(a, b):
    print(a + b )
