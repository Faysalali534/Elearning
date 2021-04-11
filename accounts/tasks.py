from datetime import timedelta

import pytz
import tzlocal
from pytz import timezone
from celery import shared_task
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from accounts.models import Test
from accounts.models import get


@shared_task
def convert_time():
    conversion, obj = get()
    tests = Test.objects.filter(pk__in=obj).all()
    for test in tests:
        local_time = tzlocal.get_localzone()
        test.my_time = test.my_time.replace(tzinfo=pytz.utc).astimezone(local_time)
        test.save()


@shared_task
def inactive_users():
    time_threshold = timezone.now() - timedelta(hours=20)
    result = User.objects.filter(Q(last_login__gt=time_threshold) | Q(last_login=None))
    if not result:
        result.update(is_active=False)
    else:
        print('No users to inactive')
