import requests
import json

from redis import Redis
from rq import Queue
q = Queue(connection=Redis())
import datetime

def check_if_passengers_cnf(passengers):
    for passenger in passengers:
        if passenger['status'] != 'CNF':
            return False
    return True


def caluclate_next_schedule_time(timenow, notification_frequency, notification_frequency_value):
    notification_frequency_value = int(notification_frequency_value)
    if notification_frequency == 'minutes':
        timenow = timenow + datetime.timedelta(minutes=notification_frequency_value)
    elif notification_frequency == 'hours':
        timenow = timenow + datetime.timedelta(hours=notification_frequency_value)
    elif notification_frequency == 'days':
        timenow = timenow + datetime.timedelta(days=notification_frequency_value)
    return timenow

def get_and_schedule_pnr_notification(pnr_notify):
    pnr_no = pnr_notify.pnr_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    resp = json.loads(resp.content)

    status = resp['status']
    data = resp['data']

    if data == {} and status == 'OK':
        return {'error': 'Something went wrong real bad! \nTry again later :)'}

    if status == "INVALID":
        return {'error': 'Invalid PNR Number!'}

    passengers = data['passenger']
    if data['chart_prepared'] or check_if_passengers_cnf(passengers):
        # The ticket is confirmed or chart prepared
        pass
    else:
        from pypnrstatus.tasks import schedule_pnr_notification
        # Put the pnr_notify into the que if not confirmed yet
        q.enqueue(schedule_pnr_notification, pnr_notify)

    return {'pnr_no': pnr_no, 'passengers': passengers}


