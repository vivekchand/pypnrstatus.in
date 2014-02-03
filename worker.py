import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import dj_database_url
if dj_database_url.config():
    settings.DATABASES['default'] =  dj_database_url.config()

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
