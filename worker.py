import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure()
import dj_database_url
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
}

if dj_database_url.config():
    settings.DATABASES['default'] =  dj_database_url.config()


from pypnrstatus.tasks import *
from pypnrstatus.models import *
from datetime import timedelta, datetime
import time

while True:
    print 'I am doing something'
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__lte=datetime.now()+timedelta(minutes=5))
    print pnr_notifications
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)
    pnr_notifications = PNRNotification.objects.filter(next_schedule_time__gte=datetime.now()-timedelta(minutes=5))
    print pnr_notifications
    for pnr_notification in pnr_notifications:
        schedule_pnr_notification(pnr_notification)

    #time.sleep(5*60)
