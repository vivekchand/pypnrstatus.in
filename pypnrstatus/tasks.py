import datetime
from pypnrstatus.pnr_utils import get_pnr_status, \
    send_ticket_cancelled_email, send_pnr_status_chart_prepared_sms, \
    send_pnr_status_confirmed_email, send_pnr_status_confirmed_sms, \
    caluclate_timedelta, send_ticket_cancelled_sms, \
    send_pnr_status_chart_prepared_email, send_pnr_status_email, send_pnr_status_sms
from exception_handler import log_exception


@log_exception
def send_pnr_notification(pnr_notify, pnr_status_dict):
    passengers = pnr_status_dict['passengers']
    notify_type = pnr_notify.notification_type
    pnr_notify.next_schedule_time = datetime.datetime.now() + caluclate_timedelta(
        pnr_notify.notification_frequency, pnr_notify.notification_frequency_value)
    pnr_notify.save()

    if pnr_status_dict['ticket_is_cancelled']:
        if notify_type == 'email':
            send_ticket_cancelled_email(passengers, pnr_notify)
        elif notify_type == 'phone':
            send_ticket_cancelled_sms(passengers, pnr_notify)
        pnr_notify.delete()
        return

    if pnr_status_dict['ticket_is_confirmed']:
        if notify_type == 'email':
            send_pnr_status_confirmed_email(passengers, pnr_notify)
        elif notify_type == 'phone':
            send_pnr_status_confirmed_sms(passengers, pnr_notify)
        pnr_notify.delete()
        return

    if pnr_status_dict['chart_prepared_for_ticket']:
        if notify_type == 'email':
            send_pnr_status_chart_prepared_email(passengers, pnr_notify)
        elif notify_type == 'phone':
            send_pnr_status_chart_prepared_sms(passengers, pnr_notify)
        pnr_notify.delete()
        return

    if pnr_notify.notification_type == 'email':
        send_pnr_status_email(passengers, pnr_notify)
    elif pnr_notify.notification_type == 'phone':
        send_pnr_status_sms(passengers, pnr_notify)

@log_exception
def schedule_pnr_notification(pnr_notify):
    pnr_status_dict = get_pnr_status(pnr_notify, delete_on_fail=False)

    if pnr_status_dict.get('error'):
       return

    send_pnr_notification(pnr_notify=pnr_notify, pnr_status_dict=pnr_status_dict)
