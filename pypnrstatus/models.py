from django.db import models
from jsonfield import JSONField

class PNRNotification(models.Model):
    pnr_no = models.CharField(max_length=20)
    notification_type = models.CharField(max_length=10)
    notification_type_value = models.CharField(max_length=50)
    notification_frequency = models.CharField(max_length=20) 
    notification_frequency_value = models.CharField(max_length=10)
    next_schedule_time = models.DateTimeField()

class PNRStatus(models.Model):
    pnr_no = models.CharField(max_length=20)
    status = JSONField()
