from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def index(request):
    if request.method == "POST":
        pnr_no = request.POST.get('pnrno')
        notification_type = request.POST.get('notification_type')
        notification_type_value = request.POST.get('email_or_phone')
        notification_frequency = request.POST.get('notification_frequency')
        notification_frequency_value = request.POST.get('notifyValue')
        return HttpResponse("Do something")
    else:
        return render(request, 'index.html')
