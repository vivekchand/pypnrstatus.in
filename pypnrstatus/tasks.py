import requests
from pypnrstatus.pnr_utils import check_if_passengers_cnf
from pypnrstatus.views import q

def schedule_pnr_notification(pnr_notify):
    pnr = pnr_notify.prn_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    resp = json.loads(resp.content)

    status = resp['status']
    data = resp['data']

    if data == {} and status == 'OK':
        # retry
        pass

    passengers = data['passenger']

    if pnr_notify.notification_type == 'email':
        # handle emailing 

    elif pnr_notify.notification_type == 'phone':
        # handle sending sms


    if data['chart_prepared'] or check_if_passengers_cnf(passengers):
        # done no more work :)
        pass 
    else:
        # Compute when to reschedule
        if pnr_notify.notification_frequency == 'minutes':
            q.enqueue()
        elif pnr_notify.notification_frequency == 'hours':
            q.enqueue()
        elif pnr_notify.notification_frequency == 'days':
            q.enqueue()



