import requests
import urllib2
from pypnrstatus.pnr_utils import *
def get_current_status(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'Passenger %s ' % i +'\n' + 'Current Status: ' + passenger['status']
        temp = temp +'\n'+ 'Seat Number:' + passenger['seat_number']+'\n\n'
        i+=1
    return temp

def schedule_pnr_notification(pnr_notify):
    pnr_no = pnr_notify.pnr_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    resp = json.loads(resp.content)

    status = resp['status']
    data = resp['data']

    if data.has_key('message'):
        return

    if data == {} and status == 'OK':
        # retry
        return

    print data
    passengers = data['passenger']

    if pnr_notify.notification_type == 'email':
        message = get_current_status(passengers)
        requests.post('https://api.mailgun.net/v2/pypnrstatus.in/messages',
            auth=("api", "key-3du65990xbf63jlr5ihvlpir2k82jqr5"),
            data={"from": "Py-PNR-Status <info@pypnrstatus.in>",
                "to": [pnr_notify.notification_type_value],
                "subject": "PNR Status %s"%pnr_no,
                "text": message})
    elif pnr_notify.notification_type == 'phone':
        message = get_current_status(passengers)
        phone = '9739788820'
        requests.get("https://160by2.p.mashape.com/index.php?msg=%s&phone=9739788820&pwd=pypnrstatus&uid=9739788820"%message,
            headers={"X-Mashape-Authorization": "SVq60zXo3xSsKhRHLseQxcpdntWwvdOx"});

    if data['chart_prepared'] or check_if_passengers_cnf(passengers):
        # done no more work :)
        # Tell ticket is confirmed / chart prepared & delete pnr_notify
        pass
    pnr_notify.next_schedule_time = pnr_notify.next_schedule_time + caluclate_timedelta(pnr_notify.notification_frequency,
                    pnr_notify.notification_frequency_value)
    pnr_notify.save()


