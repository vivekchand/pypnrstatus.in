import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pypnrstatus.settings")
from django.conf import settings

from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while False:
    print 'I am doing something'
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=1))
    print pnr_notifications
    begin = time.time()
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)
    end = time.time()
    diff = int(begin-end)
    print diff
    if diff == 0:
        sleep(1*60)
