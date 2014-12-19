from bs4 import BeautifulSoup
import requests
import re
from random import randint
from datetime import datetime


def get_correct_url():
    url = "http://www.indianrail.gov.in/pnr_Enq.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
        "Host": "www.indianrail.gov.in",
        "Origin": "http://www.indianrail.gov.in",
    }
    r = requests.get(url)
    if r.status_code == 200 :
        #then change
        soup = BeautifulSoup(r.text)
        if soup.find("form"):
            return soup.find("form")["action"]
        else:
            return False
    else:
        return False


class PnrApi:
    #url_pnr = get_correct_url()
    url_pnr = "http://www.indianrail.gov.in/cgi_bin/inet_pnstat_cgi_10521.cgi"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
        "Host": "www.indianrail.gov.in",
        "Origin": "http://www.indianrail.gov.in",
        "Referer": "http://www.indianrail.gov.in/pnr_Enq.html",
    }
    error = ""

    def __init__(self, pnr=""):
        self.response_json = {}
        if len(pnr) != 10:
            raise ValueError("PNR Number has to be of 10 digits.")
        else:
            self.pnr = pnr

    def request(self):
        request_data = {}
        random_digit = randint(10000, 99999)
        request_data["lccp_cap_val"] = random_digit
        request_data["lccp_capinp_val"] = random_digit
        request_data["lccp_pnrno1"] = self.pnr
        request_data["submit"] = "Get Status" #not required
        try:
            r = requests.post(PnrApi.url_pnr, request_data, headers=PnrApi.headers)
        except requests.exceptions.RequestException as e:
            self.error = str(e)
            return False
        if r.status_code == 404:
            self.error = "404 error, please mail contact@pnr.me to fix this issue"
            return False
        if r.text.find("Please try again later") > 0:
            self.error = "Service unavailable 23:30 to 00:30"
            return False
        elif r.text.find("FLUSHED PNR / PNR NOT YET GENERATED") > 0:
            self.error = "Wrong PNR"
            return False
        elif r.text.find("Facility Not Avbl due to Network Connectivity Failure") > 0:
            self.error = "Facility not available"
            return False
        elif r.text.find("This is circular journey authority PNR") > 0:
            self.error = "Circular Journey"
            return False
        elif r.text.find("Invalid PNR NO") > 0:
            self.error = "Invalid pnr number"
            return False
        elif r.text.find("The Train Is Cancelled") > 0:
            self.error = "Train cancelled"
            return False
        elif r.text.find("Passenger Current Status Enquiry") > 0:
            soup = BeautifulSoup(r.text)
            self.__getDetails(soup)
            return True
        else:
            self.error = "Some other error"
            return False

    def __getDetails(self, soup):
        #set pnr
        self.response_json["pnr"] = self.pnr
        #set ticket_type
        ticket_type_re = re.compile("\(.*\)")
        enq_heading = soup.find("td", {"class": "Enq_heading"}).text
        if ticket_type_re.findall(enq_heading):
            ticket_type = str(ticket_type_re.findall(enq_heading)[0])
            ticket_type = ticket_type.lstrip("\(").rstrip("\)")
        else:
            ticket_type = "Unknown"
        self.response_json["ticket_type"] = ticket_type
        #get tables
        tables = soup.findAll("table", {"class": "table_border"})
        #get journey_rows
        journey_cols = tables[0].findAll("tr")[2].findAll("td")
        #get train_number
        self.response_json["train_number"] = str(journey_cols[0].text).lstrip("*")
        #get train_name
        self.response_json["train_name"] = str(journey_cols[1].text).strip()
        #get boarding_date
        boarding_date = str(journey_cols[2].text).split("-")
        boarding_date = boarding_date[0] + "-" + boarding_date[1].strip() + "-" + boarding_date[2]
        self.response_json["boarding_date"] = datetime.strptime(boarding_date, "%d-%m-%Y")
        #get from
        self.response_json["from"] = str(journey_cols[3].text).strip()
        #get to
        self.response_json["to"] = str(journey_cols[4].text).strip()
        #get reserved_upto
        self.response_json["reserved_upto"] = str(journey_cols[5].text).strip()
        #get boarding_point
        self.response_json["boarding_point"] = str(journey_cols[6].text).strip()
        #get class
        self.response_json["class"] = str(journey_cols[7].text).strip()

        #get passengers
        passengers = []
        totalPassengers = 0
        rows = tables[1].findAll("tr")
        rowLength = len(rows)
        for i in range(1, rowLength):
            cols = rows[i].findAll("td")
            if str(cols[0].text).split()[0] == "Passenger":
                totalPassengers = totalPassengers + 1
                passengerData = {}
                booking_data = str(cols[1].text).split()
                booking_status = ""
                for element in booking_data:
                    booking_status = booking_status + " " + element
                booking_status = booking_status.strip()
                passengerData["booking_status"] = booking_status
                current_data = str(cols[2].text).split()
                current_status = ""
                for element in current_data:
                    current_status = current_status + " " + element
                current_status = current_status.strip()
                passengerData["current_status"] = current_status
                passengers.append(passengerData)
            elif str(cols[0].text).split()[0] == "Charting":
                charting_data = str(cols[1].text).split()
                charting_status = ""
                for element in charting_data:
                    charting_status = charting_status + " " + element
                charting_status = charting_status.strip()
                #get charting_status
                self.response_json["charting_status"] = charting_status
                #get total_passengers
        self.response_json["total_passengers"] = totalPassengers
        #get passenger_status
        self.response_json["passenger_status"] = passengers

    def get_json(self):
        return self.response_json


