from bs4 import BeautifulSoup
import requests
import re


def get_train_schedule(self, soup):
    tables = soup.find_all("table", {"class": "table_border_both"})
    if tables:
        train_info = tables[0]  # assumption. first four values train no, train name and source and days
        schedule_table = train_info.find("tr", {"class": None})
        if schedule_table:
            row = schedule_table.find_all("td")
            self.response_json['train_number'] = [str(row[0].text.strip())]
            self.response_json['train_name'] = str(row[1].text.strip())
            self.response_json['source'] = str(row[2].text.strip())
            days_available = []
            for day in range(3, len(row)):
                days_available.append(str(row[day].text.strip()))
            self.response_json['days available'] = days_available

            #split into list of classes
            schedule_info = tables[1]
            schedule_rows = schedule_info.find_all("tr", {"class": None})
            schedule_array = []
            for schedule in schedule_rows:
                schedule_object = {}
                values = schedule.find_all("td")
                if len(values) == 1:
                    number = re.compile('\d+')
                    train_number = number.findall(str(values[0].text))
                    if train_number:
                        self.response_json['train_number'].append(train_number[0])
                if len(values) > 8:
                    schedule_object["sno"] = str(values[0].text.strip())
                    schedule_object["station code"] = str(values[1].text.strip())
                    schedule_object["station name"] = str(values[2].text.strip())
                    schedule_object["route number"] = str(values[3].text.strip())
                    schedule_object["arrival time"] = str(values[4].text.strip())
                    schedule_object["departure time"] = str(values[5].text.strip())
                    schedule_object["time halt"] = str(values[6].text.strip())
                    schedule_object["distance"] = str(values[7].text.strip())
                    schedule_object["day"] = str(values[8].text.strip())
                    if len(values) > 9:
                        schedule_object["remarks"] = str(values[9].text.strip())
                    else:
                        schedule_object["remarks"] = ""
                    schedule_array.append(schedule_object)
            self.response_json['schedule'] = schedule_array
            return self
        else:
            self.error = "Schedule not available"
            return self


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


class TrainSearch:
    url = "http://www.indianrail.gov.in/cgi_bin/inet_trnnum_cgi.cgi"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0",
        "Host": "www.indianrail.gov.in",
        "Origin": "http://www.indianrail.gov.in",
        "Referer": "http://www.indianrail.gov.in/inet_trn_num.html"
    }
    error = ""

    def __init__(self, train_name):
        self.response_json = {}
        self.train_name = train_name

    def request(self):
        request_data = {
            "getIt": "Get Schedule",
            "lccp_trnname": self.train_name,
        }
        try:
            r = requests.post(self.url, request_data, headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.error = str(e)
            return False
        if r.text.find("Please try again later") > 0:
            self.error = "Service unavailable"
            return False
        elif r.text.find("Facility Not Avbl due to Network Connectivity Failure") > 0:
            self.error = "Facility not available"
            return False
        elif r.text.find("SORRY !!! No Matching Trains Found") > 0:
            self.error = "No Matching trains found"
            return False
        elif r.text.find("TRAIN ROUTE") > 0:
            soup = BeautifulSoup(r.text)
            get_train_schedule(self, soup)
            self.response_json["return_type"] = "schedule"
            if self.error:
                return False
            else:
                return True
        elif r.text.find("Train Names with Details") > 0:
            soup = BeautifulSoup(r.text)
            get_train_list(self, soup)
            self.response_json["return_type"] = "train list"
            if self.error:
                return False
            else:
                return True
        else:
            self.error = "Some other error"
            return False


    def get_json(self):
        return self.response_json