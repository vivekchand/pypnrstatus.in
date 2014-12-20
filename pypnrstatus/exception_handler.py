
def log_exception(func):
    def send_mail_on_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            import sys, cgitb
            from pnr_utils import send_email
            send_email(
                message=u'{} \n\n {}'.format(e.message, cgitb.html(sys.exc_info())),
                subject='Py-PNR-Status Error!',
                to_addr='vivekchand19@gmail.com'
            )
            raise
    return send_mail_on_exception

