import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pypnrstatus.settings")
from django.conf import settings

from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while True:
    try:
        print 'I am doing something'
        pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=5))
        print pnr_notifications
        begin = time.time()
        for pnr_notification in pnr_notifications:
            schedule_pnr_notification(pnr_notification)
        end = time.time()
        diff = int(end-begin)
        sleep_time = int((5*60) - (diff/60))
        print 'sleeping for %s min' % (sleep_time/60)
        if sleep_time>0:
            time.sleep(sleep_time)
    except:
        # Send email/sms notification to me.
        pass
