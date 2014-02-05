import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pypnrstatus.settings")
from django.conf import settings

from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while True:
    print 'I am doing something'
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=5),
        next_schedule_time__gte=datetime.now()-timedelta(minutes=5))
    print pnr_notifications
    #start = time.time()
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)
    '''
    end = time.time()
    diff = int(end-start)
    sleep_time = (5*60)-(diff/60)
    print 'sleep time: %s min'% (sleep_time/60)
    if sleep_time>0:
        time.sleep(sleep_time)
    '''
    pass
