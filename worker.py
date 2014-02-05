import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pypnrstatus.settings")
from django.conf import settings

from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while True:
    print 'I am doing something'
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=1),
            next_schedule_time__gte=datetime.now()-timedelta(minutes=1))
    print pnr_notifications
    begin = time.time()
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)
    end = time.time()
    sleep_time = int(end-begin)
    print 'sleep time %s' % sleep_time
    print 'sleeping for 1 min'
    time.sleep(1*60)
