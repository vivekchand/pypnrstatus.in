from django.conf import settings
if not settings.configured:
    settings.configure()

from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while True:
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=5))
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)
    time.sleep(5*60) 
