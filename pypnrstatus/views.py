from django.conf import settings
if not settings.configured:
    settings.configure()

from django.http import HttpResponseRedirect
from django.shortcuts import render
from pypnrstatus.models import PNRNotification
from pypnrstatus.pnr_utils import get_pnr_status, caluclate_timedelta
from pypnrstatus.tasks import send_pnr_notification
import datetime

def index(request):
    return render(request, 'index.html')

def pnr_status(request):
    if request.method == "POST":
        pnr_no = request.POST.get('pnrno')
        notification_type = request.POST.get('notification_type')
        notification_type_value = request.POST.get('email_or_phone')
        notification_frequency = request.POST.get('notification_frequency')
        notification_frequency_value = request.POST.get('notifyValue')

        timenow = datetime.datetime.now()

        next_schedule_time =  timenow + caluclate_timedelta(notification_frequency,
                notification_frequency_value)

        pnr_no = pnr_no[:10]
        try:
            pnr_notify = PNRNotification.objects.get(pnr_no=pnr_no)
            pnr_notify.notification_type = notification_type
            pnr_notify.notification_type_value = notification_type_value
            pnr_notify.notification_frequency = notification_frequency
            pnr_notify.notification_frequency_value = notification_frequency_value
            pnr_notify.next_schedule_time = next_schedule_time
            pnr_notify.save()
        except PNRNotification.DoesNotExist:
            pnr_notify = PNRNotification.objects.create( pnr_no=pnr_no, notification_type=notification_type,
                notification_type_value=notification_type_value, notification_frequency=notification_frequency,
                notification_frequency_value=notification_frequency_value, next_schedule_time=next_schedule_time )

        pnr_status = get_pnr_status(pnr_notify)
        send_pnr_notification(pnr_notify=pnr_notify, pnr_status_dict=pnr_status)
        return render(request, 'pnr_status.html', pnr_status)
    else:
        return HttpResponseRedirect('/')

def stop_notifications(request):
    pnr_no = request.GET.get('pnrno')
    if pnr_no:
        try:
            pnr_notify = PNRNotification.objects.get(pnr_no=pnr_no)
            pnr_notify.delete()
            return render(request, 'stop_notifications.html', {'message':'Successfully Unsubscribed from pypnrstatus.in notifications!'})
        except:
            return render(request, 'stop_notifications.html', {'message': 'No such PNR number!'})
    else:
        return render(request, 'stop_notifications.html')
