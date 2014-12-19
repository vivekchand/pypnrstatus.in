pnrapi-python
=============

A Python web-scraper for Indian Railways' PNR Status and Train Schedule.

Requirements
------------
* [Beautiful Soup 4][1]
  - `pip install beautifulsoup4` or `easy_install beautifulsoup4`
* [Requests][2]
  - `pip install requests` or `easy_install requests`

Sample Request for PNR status
--------------
	import pnrapi
	p = pnrapi.PnrApi("1234567890") #10-digit PNR Number
	if p.request() == True:
		response = p.get_json()
		print response
	else:
		print "Service unavailable"

Sample Response for PNR status
---------------
The reponse is a json object as follows:

	{
		'pnr': '1234567890',
		'ticket_type': 'E - TICKET',
		'train_number': '12230'
		'train_name': 'LUCKNOW MAIL',
		'boarding_date': datetime.datetime(2013, 11, 9, 0, 0),
		'from': 'NDLS',
		'to': 'LKO',
		'reserved_upto': 'LKO',
		'boarding_point': 'NDLS',
		'class': '3A',
		'total_passengers': 1,
		'charting_status': 'CHART PREPARED',
		'passenger_status': [
			{'booking_status': 'W/L 10,GNWL', 'current_status': 'B4 , 17'}
		]
	}
The `passenger_status` array will contain `total_passengers` number of elements.

Sample Request for Train Schedule
--------------
    import train_schedule
    train = train_schedule.TrainSchedule("12906", "10", "2")#month and day are highly recommended
    if train.request() == True:
        print train.get_json()
    else:
        print train.error

Sample Response for Train Schedule
---------------
The reponse is a json object as follows:

    {
       'source':'HOWRAH JN',
       'days available':[
          'TUE',
          'FRI',
          'SAT'
       ],
       'train_name':'HWH PBR  OKHAEX',
       'train_number':[
          '12906',
          '22906'
       ],
       'schedule':[
          {
             'time halt':'',
             'station code':'HWH',
             'sno':'1',
             'arrival time':'Source',
             'station name':'HOWRAH JN',
             'remarks':'',
             'departure time':'22:55',
             'day':'1',
             'route number':'1',
             'distance':'0'
          },
          {
             'time halt':'5:00',
             'station code':'KGP',
             'sno':'2',
             'arrival time':'00:35',
             'station name':'KHARAGPUR JN',
             'remarks':'',
             'departure time':'00:40',
             'day':'2',
             'route number':'1',
             'distance':'116'
          },
          {
             'time halt':'5:00',
             'station code':'TATA',
             'sno':'3',
             'arrival time':'02:30',
             'station name':'TATANAGAR JN',
             'remarks':'',
             'departure time':'02:35',
             'day':'2',
             'route number':'1',
             'distance':'250'
          },
          {
             'time halt':'5:00',
             'station code':'CKP',
             'sno':'4',
             'arrival time':'03:30',
             'station name':'CHAKRADHARPUR',
             'remarks':'',
             'departure time':'03:35',
             'day':'2',
             'route number':'1',
             'distance':'312'
          },
          {
             'time halt':'7:00',
             'station code':'ROU',
             'sno':'5',
             'arrival time':'04:53',
             'station name':'ROURKELA',
             'remarks':'',
             'departure time':'05:00',
             'day':'2',
             'route number':'1',
             'distance':'413'
          },
          {
             'time halt':'2:00',
             'station code':'JSG',
             'sno':'6',
             'arrival time':'06:28',
             'station name':'JHARSUGUDA JN',
             'remarks':'',
             'departure time':'06:30',
             'day':'2',
             'route number':'1',
             'distance':'515'
          },
          {
             'time halt':'2:00',
             'station code':'RIG',
             'sno':'7',
             'arrival time':'07:19',
             'station name':'RAIGARH',
             'remarks':'',
             'departure time':'07:21',
             'day':'2',
             'route number':'1',
             'distance':'588'
          },
          {
             'time halt':'2:00',
             'station code':'CPH',
             'sno':'8',
             'arrival time':'08:13',
             'station name':'CHAMPA',
             'remarks':'',
             'departure time':'08:15',
             'day':'2',
             'route number':'1',
             'distance':'668'
          },
          {
             'time halt':'15:00',
             'station code':'BSP',
             'sno':'9',
             'arrival time':'09:25',
             'station name':'BILASPUR JN',
             'remarks':'',
             'departure time':'09:40',
             'day':'2',
             'route number':'1',
             'distance':'720'
          },
          {
             'time halt':'1:00',
             'station code':'BYT',
             'sno':'10',
             'arrival time':'10:17',
             'station name':'BHATAPARA',
             'remarks':'',
             'departure time':'10:18',
             'day':'2',
             'route number':'1',
             'distance':'767'
          },
          {
             'time halt':'10:00',
             'station code':'R',
             'sno':'11',
             'arrival time':'11:20',
             'station name':'RAIPUR JN',
             'remarks':'',
             'departure time':'11:30',
             'day':'2',
             'route number':'1',
             'distance':'831'
          },
          {
             'time halt':'5:00',
             'station code':'DURG',
             'sno':'12',
             'arrival time':'12:20',
             'station name':'DURG',
             'remarks':'',
             'departure time':'12:25',
             'day':'2',
             'route number':'1',
             'distance':'867'
          },
          {
             'time halt':'2:00',
             'station code':'RJN',
             'sno':'13',
             'arrival time':'12:46',
             'station name':'RAJ NANDGAON',
             'remarks':'',
             'departure time':'12:48',
             'day':'2',
             'route number':'1',
             'distance':'897'
          },
          {
             'time halt':'2:00',
             'station code':'G',
             'sno':'14',
             'arrival time':'14:13',
             'station name':'GONDIA JN',
             'remarks':'',
             'departure time':'14:15',
             'day':'2',
             'route number':'1',
             'distance':'1001'
          },
          {
             'time halt':'10:00',
             'station code':'NGP',
             'sno':'15',
             'arrival time':'16:20',
             'station name':'NAGPUR',
             'remarks':'',
             'departure time':'16:30',
             'day':'2',
             'route number':'1',
             'distance':'1131'
          },
          {
             'time halt':'5:00',
             'station code':'BD',
             'sno':'16',
             'arrival time':'19:10',
             'station name':'BADNERA JN',
             'remarks':'',
             'departure time':'19:15',
             'day':'2',
             'route number':'1',
             'distance':'1305'
          },
          {
             'time halt':'5:00',
             'station code':'AK',
             'sno':'17',
             'arrival time':'20:05',
             'station name':'AKOLA JN',
             'remarks':'',
             'departure time':'20:10',
             'day':'2',
             'route number':'1',
             'distance':'1384'
          },
          {
             'time halt':'10:00',
             'station code':'BSL',
             'sno':'18',
             'arrival time':'21:55',
             'station name':'BHUSAVAL JN',
             'remarks':'',
             'departure time':'22:05',
             'day':'2',
             'route number':'1',
             'distance':'1524'
          },
          {
             'time halt':'5:00',
             'station code':'NDB',
             'sno':'19',
             'arrival time':'01:55',
             'station name':'NANDURBAR',
             'remarks':'',
             'departure time':'02:00',
             'day':'3',
             'route number':'1',
             'distance':'1699'
          },
          {
             'time halt':'10:00',
             'station code':'ST',
             'sno':'20',
             'arrival time':'04:55',
             'station name':'SURAT',
             'remarks':'',
             'departure time':'05:05',
             'day':'3',
             'route number':'1',
             'distance':'1859'
          },
          {
             'time halt':'5:00',
             'station code':'BRC',
             'sno':'21',
             'arrival time':'06:50',
             'station name':'VADODARA JN',
             'remarks':'',
             'departure time':'06:55',
             'day':'3',
             'route number':'1',
             'distance':'1988'
          },
          {
             'time halt':'1:00',
             'station code':'ANND',
             'sno':'22',
             'arrival time':'07:28',
             'station name':'ANAND JN',
             'remarks':'',
             'departure time':'07:29',
             'day':'3',
             'route number':'1',
             'distance':'2024'
          },
          {
             'time halt':'20:00',
             'station code':'ADI',
             'sno':'23',
             'arrival time':'08:55',
             'station name':'AHMEDABAD JN',
             'remarks':'',
             'departure time':'09:15',
             'day':'3',
             'route number':'1',
             'distance':'2087'
          },
          {
             'time halt':'1:00',
             'station code':'VG',
             'sno':'24',
             'arrival time':'10:21',
             'station name':'VIRAMGAM JN',
             'remarks':'',
             'departure time':'10:22',
             'day':'3',
             'route number':'1',
             'distance':'2153'
          },
          {
             'time halt':'1:00',
             'station code':'SUNR',
             'sno':'25',
             'arrival time':'11:27',
             'station name':'SURENDRANAGAR',
             'remarks':'',
             'departure time':'11:28',
             'day':'3',
             'route number':'1',
             'distance':'2218'
          },
          {
             'time halt':'5:00',
             'station code':'RJT',
             'sno':'26',
             'arrival time':'13:31',
             'station name':'RAJKOT JN',
             'remarks':'',
             'departure time':'13:36',
             'day':'3',
             'route number':'1',
             'distance':'2334'
          },
          {
             'time halt':'34:00',
             'station code':'HAPA',
             'sno':'27',
             'arrival time':'14:51',
             'station name':'HAPA',
             'remarks':'',
             'departure time':'15:25',
             'day':'3',
             'route number':'1',
             'distance':'2410'
          },
          {
             'time halt':'5:00',
             'station code':'JAM',
             'sno':'28',
             'arrival time':'15:35',
             'station name':'JAMNAGAR',
             'remarks':'',
             'departure time':'15:40',
             'day':'3',
             'route number':'1',
             'distance':'2419'
          },
          {
             'time halt':'1:00',
             'station code':'LPJ',
             'sno':'29',
             'arrival time':'16:46',
             'station name':'LALPUR JAM',
             'remarks':'',
             'departure time':'16:47',
             'day':'3',
             'route number':'1',
             'distance':'2462'
          },
          {
             'time halt':'',
             'station code':'PBR',
             'sno':'30',
             'arrival time':'19:00',
             'station name':'PORBANDAR',
             'remarks':'',
             'departure time':'Destination',
             'day':'3',
             'route number':'1',
             'distance':'2551'
          },
          {
             'time halt':'89:00',
             'station code':'HAPA',
             'sno':'31',
             'arrival time':'14:51',
             'station name':'HAPA',
             'remarks':'',
             'departure time':'16:20',
             'day':'3',
             'route number':'2',
             'distance':'2410'
          },
          {
             'time halt':'1:00',
             'station code':'KMBL',
             'sno':'32',
             'arrival time':'17:45',
             'station name':'KHAMBHALIYA',
             'remarks':'',
             'departure time':'17:46',
             'day':'3',
             'route number':'2',
             'distance':'2473'
          },
          {
             'time halt':'1:00',
             'station code':'DWK',
             'sno':'33',
             'arrival time':'18:58',
             'station name':'DWARKA',
             'remarks':'',
             'departure time':'18:59',
             'day':'3',
             'route number':'2',
             'distance':'2557'
          },
          {
             'time halt':'',
             'station code':'OKHA',
             'sno':'34',
             'arrival time':'20:00',
             'station name':'OKHA',
             'remarks':'',
             'departure time':'Destination',
             'day':'3',
             'route number':'2',
             'distance':'2586'
          }
       ]
    }
The `schedule` array will contain array of schedule objects
Train number is an array because. Trains can have multiple slip routes


[1]: http://www.crummy.com/software/BeautifulSoup/
[2]: https://github.com/kennethreitz/requests
