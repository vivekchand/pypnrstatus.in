from bs4 import BeautifulSoup
import requests
import re


def get_train_list(self, soup):
    tables = soup.find_all("table", {"class": "table_border_both"})
    if len(tables) > 0:
        train_info = tables[0]  # assumption. first four values train no, train name and source and days
        train_list = train_info.find_all("tr", {"class": None})
        self.response_json['trains'] = []
        for train in train_list:
            row = train.find_all("td")
            if len(row) > 5:
                self.response_json['trains'].append({
                    "train_number": str(row[0].text.strip()),
                    "train_name": str(row[1].text.strip()),
                    "source": str(row[2].text.strip()),
                    "departure_time": str(row[3].text.strip()),
                    "destination": str(row[4].text.strip()),
                    "arrival_time": str(row[5].text.strip())
                })
        if len(self.response_json['trains']) == 0:
            self.error = "Train list not available"
        return self


class TrainBetweenStations:
    url = "http://www.indianrail.gov.in/cgi_bin/inet_srcdest_cgi.cgi"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
        "Host": "www.indianrail.gov.in",
        "Origin": "http://www.indianrail.gov.in",
        "Referer": "http://www.indianrail.gov.in/inet_Srcdest.html"
    }
    error = ""

    def __init__(self, source, destination, travel_class="ZZ"):
        self.response_json = {}
        self.source = source
        self.destination = destination
        self.travel_class = travel_class

    def request(self):
        request_data = {
            "lccp_src_stncode": self.source,
            "lccp_src_stncode_dis": "",
            "lccp_dstn_stncode": self.destination,
            "lccp_dstn_stncode_dis": "",
            "lccp_classopt": self.travel_class,
            "CurrentMonth": "4",
            "CurrentDate": "19",
            "CurrentYear": "2006"
        }
        try:
            r = requests.post(self.url, request_data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.error = str(e)
            return False
        if r.text.find("The Station Code is Invalid") > 0:
            self.error = "Incorrect Station code"
            return False
        if r.text.find("Please fill in all of the fields in the form.") > 0:
            self.error = "Incomplete Details"
            return False
        elif r.text.find("Facility Not Avbl due to Network Connectivity Failure") > 0:
            self.error = "Facility not available"
            return False
        elif r.text.find("SORRY !!! No Matching Trains Found") > 0:
            self.error = "No Matching trains found"
            return False
        elif r.text.find("Trains Between A Pair of Stations") > 0:
            soup = BeautifulSoup(r.text)
            get_train_list(self, soup)
            self.response_json["return_type"] = "schedule"
            if self.error:
                return False
            else:
                return True
        else:
            self.error = "Some other error"
            return False


    def get_json(self):
        return self.response_json