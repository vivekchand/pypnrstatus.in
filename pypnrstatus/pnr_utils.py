import requests
import json

import datetime

def check_if_passengers_cnf(passengers):
    for passenger in passengers:
        if passenger['status'] != 'CNF':
            return False
    return True

def check_if_ticket_cancelled(passengers):
    cancel_count = 0
    total_count = len(passengers)
    for passenger in passengers:
        if passenger['status'] == 'Can/Mod':
            cancel_count += 1
    if cancel_count == total_count:
        return True
    return False


def caluclate_timedelta(notification_frequency, notification_frequency_value):
    notification_frequency_value = int(notification_frequency_value)
    if notification_frequency == 'minutes':
        timedelta = datetime.timedelta(minutes=notification_frequency_value)
    elif notification_frequency == 'hours':
        timedelta = datetime.timedelta(hours=notification_frequency_value)
    elif notification_frequency == 'days':
        timedelta = datetime.timedelta(days=notification_frequency_value)
    return timedelta


def schedule_notification_now(pnr_notify):
    now = datetime.datetime.now()
    timedelta = caluclate_timedelta('minutes', 1)
    pnr_notify.next_schedule_time = now + timedelta
    pnr_notify.save()

def get_pnr_status(pnr_notify):
    pnr_no = pnr_notify.pnr_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    try:
        resp = json.loads(resp.content)
    except ValueError:
        pnr_notify.delete()
        return {'error': "We couldn't process your request for pnr no %s at this time!"% pnr_no}

    status = resp['status']
    data = resp['data']

    print data
    if data.has_key('message'):
        pnr_notify.delete()
        print data['message']
        return {'error': "We couldn't process your request for pnr no %s at this time!"% pnr_no}

    if data == {} and status == 'OK':
        pnr_notify.delete()
        return {'error': "We couldn't process your request for pnr no %s at this time!"% pnr_no}

    if status == "INVALID":
        pnr_notify.delete()
        return {'error': 'Invalid PNR Number %s!'% prn_no}

    passengers = data['passenger']

    ticket_is_cancelled = ticket_is_confirmed = chart_prepared_for_ticket = None
    will_get_notifications = True

    if check_if_ticket_cancelled(passengers):
        ticket_is_cancelled = True
        will_get_notifications = False
        schedule_notification_now(pnr_notify)
    if check_if_passengers_cnf(passengers):
        ticket_is_confirmed = True
        will_get_notifications = False
        schedule_notification_now(pnr_notify)
    if data['chart_prepared']:
        chart_prepared_for_ticket = True
        will_get_notifications = False
        schedule_notification_now(pnr_notify)

    json_dict =  {'pnr_no': pnr_no,
                  'passengers': passengers,
                  'ticket_is_cancelled': ticket_is_cancelled,
                  'ticket_is_confirmed': ticket_is_confirmed,
                  'chart_prepared_for_ticket': chart_prepared_for_ticket,
                  'will_get_notifications': will_get_notifications,
                  'pnr_notify': pnr_notify }
    return json_dict


def get_current_status(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'Passenger %s ' % i +'<br/>' + 'Current Status: ' + passenger['status']
        temp = temp +'<br/>'+ 'Seat Number: ' + passenger['seat_number']+'<br/><br/>'
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


def send_email(message, subject, to_addr):
    print 'sending'
    requests.post('https://api.mailgun.net/v2/pypnrstatus.in/messages',
        auth=("api", "key-3du65990xbf63jlr5ihvlpir2k82jqr5"),
        data={"from": "Py-PNR-Status <info@pypnrstatus.in>",
            "to": [to_addr],
            "subject": subject,
            "html": message})
    print 'sent :)'


def send_sms(message, phone_no):
    print 'sending'
    import plivo
    p = plivo.RestAPI('MAMDBMM2YYNTEXYMMWZJ', 'MjM2OWI2ZjA4YmE0ZjQzYzY4ZmFmY2RlNDJmZDlk')
    plivo_number = '910123456789'
    if len(phone_no) == 10:
        phone_no = '91'+phone_no
    message_params = {
      'src':plivo_number,
      'dst':phone_no,
      'text':message,
    }
    print p.send_message(message_params)
    print 'sent :)'

# email helpers
def send_pnr_status_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    unsubscribe_link = "<a href='pypnrstatus.in/stop_notifications/?pnrno=%s'>Unsubscribe (Stop Notifications)</a>"%pnr_no
    message += '<br/><br/>' + unsubscribe_link
    subject = "PNR Status %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_email(message, subject, to_addr)

def send_pnr_status_chart_prepared_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Chart Prepared for PNR %s</b> <br/><br/>' % pnr_notify.pnr_no) + message
    subject = "Chart Prepared for PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_email(message, subject, to_addr)

def send_pnr_status_confirmed_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Ticket Confirmed for PNR %s  :)</b> <br/><br/>' % pnr_notify.pnr_no)  + message
    subject = "PNR Status Confirmed! PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_email(message, subject, to_addr)

def send_tatkal_ticket_book_email(passengers, pnr_notify):
    pass

def send_ticket_cancelled_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Your ticket with PNR %s was cancelled!</b> <br/><br/>' % pnr_notify.pnr_no) + message
    subject = "Your ticket was cancelled! PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_email(message, subject, to_addr)

# sms helpers
def send_pnr_status_sms(passengers, pnr_notify):
    message = 'PNR %s\n'% pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    message += '\n- pypnrstatus.in'
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_pnr_status_chart_prepared_sms(passengers, pnr_notify):
    message = 'Chart prepared for PNR %s\n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_pnr_status_confirmed_sms(passengers, pnr_notify):
    message = 'Ticket CNF for PNR %s\n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_tatkal_ticket_book_sms(passengers, pnr_notify):
    pass

def send_ticket_cancelled_sms(passengers, pnr_notify):
    message = 'Ticket Cancelled for PNR %s \n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)
