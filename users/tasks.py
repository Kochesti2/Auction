# Create your tasks here
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import shared_task
from celery.task import periodic_task
from django.utils import timezone
from django.utils.datetime_safe import datetime
from products.models import Product

# celery -A Auction worker -B --loglevel=INFO
# heroku.com

@periodic_task(run_every=timedelta(seconds=20))
def every_20_seconds():

    all_products = Product.objects.all()
    for p in all_products:
        if p.end_date < datetime.date(timezone.localtime(timezone.now())):
            p.disponible = False
        else:
            p.disponible = True
        p.save()
    print(all_products)

    print("Running periodic task!")

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

