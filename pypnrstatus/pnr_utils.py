import requests
import json

def check_if_passengers_cnf(passengers):
    for passenger in passengers:
        if passenger['status'] != 'CNF':
            return False
    return True


def get_and_schedule_pnr_notification(pnr_notify):
    pnr_no = pnr_notify.pnr_no
    resp = requests.get('http://pnrapi.alagu.net/api/v1.0/pnr/%s'%pnr_no)
    resp = json.loads(resp.content)        

    status = resp['status']
    data = resp['data']
    
    if data == {} and status == 'OK':
        return {'error': 'Something went wrong real bad! Try again Later :)'}
    
    if status == "INVALID":
        return {'error': 'Invalid PNR Number!'}
    
    passengers = data['passenger']
    if data['chart_prepared'] or check_if_passengers_cnf(passengers):
        # The ticket is confirmed or chart prepared
        pass    
    else:        
        # Put the pnr_notify into the worker que if not confirmed yet
        pass

    return {'pnr_no': pnr_no, 'passengers': passengers}


