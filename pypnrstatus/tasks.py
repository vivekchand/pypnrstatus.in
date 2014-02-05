import requests
import urllib2
from pypnrstatus.pnr_utils import *
import datetime
def get_current_status(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'Passenger %s ' % i +'<br/>' + 'Current Status: ' + passenger['status']
        temp = temp +'<br/>'+ 'Seat Number:' + passenger['seat_number']+'<br/><br/>'
        i+=1
    return temp

def get_current_status_sms(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'P%s ' % i +'\n' + 'Curr Stat.: ' + passenger['status']
        temp = temp +'\n'+ 'SNo:' + passenger['seat_number']+'\n\n'
        i+=1
    return temp


def schedule_pnr_notification(pnr_notify):
    pnr_no = pnr_notify.pnr_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    resp = json.loads(resp.content)

    pnr_notify.next_schedule_time = datetime.datetime.now() + caluclate_timedelta(pnr_notify.notification_frequency,
                    pnr_notify.notification_frequency_value)
    pnr_notify.save()

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
        print 'sending email ...'
        message = get_current_status(passengers)
        unsubscribe_link = "<a href='pypnrstatus.in/stop_notifications/?pnrno=%s'>Unsubscribe (Stop Notifications)</a>"%pnr_no
        message += '<br/><br/>' + unsubscribe_link
        requests.post('https://api.mailgun.net/v2/pypnrstatus.in/messages',
            auth=("api", "key-3du65990xbf63jlr5ihvlpir2k82jqr5"),
            data={"from": "Py-PNR-Status <info@pypnrstatus.in>",
                "to": [pnr_notify.notification_type_value],
                "subject": "PNR Status %s"%pnr_no,
                "html": message})
        print 'sent :)'
    elif pnr_notify.notification_type == 'phone':
        print 'sending sms ...'
        import plivo
        p = plivo.RestAPI('MAMDBMM2YYNTEXYMMWZJ', 'MjM2OWI2ZjA4YmE0ZjQzYzY4ZmFmY2RlNDJmZDlk')
        plivo_number = '910123456789'
        message = get_current_status_sms(passengers)
        message += '\n- pypnrstatus.in'
        if len(pnr_notify.notification_type_value) == 10:
            pnr_notify.notification_type_value = '91'+pnr_notify.notification_type_value
        destination_number = pnr_notify.notification_type_value
        message_params = {
          'src':plivo_number,
          'dst':destination_number,
          'text':message,
        }
        print p.send_message(message_params)
        print 'sent :)'

    if data['chart_prepared'] or check_if_passengers_cnf(passengers):
        # done no more work :)
        # Tell ticket is confirmed / chart prepared & delete pnr_notify
        pass


