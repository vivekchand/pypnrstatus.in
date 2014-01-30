from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from pypnrstatus.models import PNRNotification
from pypnrstatus.pnr_utils import get_and_schedule_pnr_notification

def index(request):
    if request.method == "POST":
        pnr_no = request.POST.get('pnrno')
        notification_type = request.POST.get('notification_type')
        notification_type_value = request.POST.get('email_or_phone')
        notification_frequency = request.POST.get('notification_frequency')
        notification_frequency_value = request.POST.get('notifyValue')

        pnr_notify = PNRNotification.objects.create( pnr_no=pnr_no, notification_type=notification_type,
            notification_type_value=notification_type_value, notification_frequency=notification_frequency,
            notification_frequency_value=notification_frequency_value )

        pnr_status = get_and_schedule_pnr_notification(pnr_notify)
        return render(request, 'pnr_status.html', pnr_status)
    else:
        return render(request, 'index.html')
