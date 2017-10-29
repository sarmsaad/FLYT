import pytz
from flask import Flask, request, jsonify
from tasks import blah
import requests
import csv

app = Flask(__name__)

APP_KEY_DISTANCE = 'AIzaSyALWTLc32yxdQyw0kt3t1BwUNpcT7sp1mI'
APP_KEY_GOECODE = 'AIzaSyAWOFkVAIf0S3uUAQ6umYkwMprlQweag24'
distanceMatrix_root = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'
geocode_root = 'https://maps.googleapis.com/maps/api/geocode/json?'

users = []

Airports = {'ATL': 'Hartsfield–Jackson Atlanta International Airport, Atlanta, GA',
            'LAX': 'Los Angeles International Airport, Los Angeles, CA',
            'ORD': "O'Hare International Airport, Chicago, IL",
            'DFW': 'Dallas/Fort Worth International Airport, Dallas/Fort Worth, TX',
            'JFK': 'John F. Kennedy International Airport, New York, NY',
            'DEN': 'Denver International Airport, Denver, CO',
            'SFO': 'San Francisco International Airport, San Francisco, CA',
            'LAS': 'McCarran International Airport, Las Vegas, NV',
            'SEA': 'Seattle–Tacoma International Airport, Seattle/Tacoma, WA',
            'CLT': 'Charlotte Douglas International Airport, Charlotte, NC',
            'PHX': 'Phoenix Sky Harbor International Airport, Phoenix, AZ',
            'MIA': 'Miami International Airport, Miami, FL', 'MCO': 'Orlando International Airport, Orlando, FL',
            'IAH': 'George Bush Intercontinental Airport, Houston, TX',
            'EWR': 'Newark Liberty International Airport, Newark/New Jersey, NJ',
            'MSP': 'Minneapolis–Saint Paul International Airport, Minneapolis/St. Paul, MN',
            'BOS': 'Logan International Airport, Boston, MA', 'DTW': 'Detroit Metropolitan Airport, Detroit, MI',
            'PHL': 'Philadelphia International Airport, Philadelphia, PA', 'LGA': 'LaGuardia Airport, New York, NY',
            'FLL': 'Fort Lauderdale–Hollywood International Airport, Fort Lauderdale/Miami, FL',
            'BWI': 'Baltimore–Washington International Airport, Baltimore/Washington, D.C., MD',
            'DCA': 'Ronald Reagan Washington National Airport, Washington, D.C., VA',
            'SLC': 'Salt Lake City International Airport, Salt Lake City, UT',
            'MDW': 'Midway International Airport, Chicago, IL',
            'IAD': 'Washington Dulles International Airport, Washington, D.C., VA',
            'SAN': 'San Diego International Airport, San Diego, CA',
            'HNL': 'Daniel K. Inouye International Airport, Honolulu, HI',
            'TPA': 'Tampa International Airport, Tampa, FL', 'PDX': 'Portland International Airport, Portland, OR'}

from redis import Redis
from rq_scheduler import Scheduler

from twilio.rest import TwilioRestClient
from datetime import datetime, timedelta

# intialize the server
redis_server = Redis()

# intiliaze the scheduler
scheduler = Scheduler(connection=redis_server)

TWILIO_ACCOUNT_SID = 'ACd3d6e4fed0307c74bd8db2d07d9f4e3b'
TWILIO_AUTH_TOKEN = 'df0c48d047e18a0b816e5dba110dd9ed'
TNUM = "+19712703263"
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route('/subscribe', methods=['GET', "POST"])
def storeInfo():
    rr = dict(request.args)
    origin = rr['address'][0]
    phoneNumber = rr['phone'][0]
    flightNumber = rr['flightNumber'][0]
    flightTime = rr['flightTime'][0]
    departureDay = int(rr['departureDay'][0])
    airport = rr['destination'][0]
    transport = rr['transportation'][0]
    checkin = rr['checkin'][0]
    person = user(phoneNumber, origin, flightNumber, flightTime, airport, transport, checkin, departureDay)
    add_to_queue(person)
    return jsonify(rr)


@app.route('/changeOri', methods=['POST'])
def changeOrigin():
    origin = request.form['address']
    phoneNumber = request.form['phone number']
    ##here we search for the use that has the following phone number and change their origin so
    ##we need to calculate their leaving time from their location has changed
    for i in users:
        if phoneNumber == i.phone:
            i.changeDestination(origin)
            return i.estimateTime
    return "sorry didn't find the user"


class user:
    def __init__(self, phoneNumber, address, flightNumber, flightTime, airport, transport, checkin, depart):
        self.phone = phoneNumber
        self.address = address
        self.flight = flightNumber
        self.time = flightTime
        self.airport = Airports[airport]
        self.transport = transport
        self.checkin = checkin
        ##this is the most important variable
        # needs more estimations to get an accurate leaving time
        self.estimateTime = getAverageTravelTime(address, airport, transport)
        self.departure = depart

    def changeDestination(self, origin):
        ##do somechanges.
        self.estimateTime = self.estimateTime - getAverageTravelTime(self.address, self.airport,
                                                                     self.transport) + getAverageTravelTime(origin,
                                                                                                            self.airport,
                                                                                                            self.transport)
        self.address = origin


def getAverageTravelTime(origin, destination, transport):
    ##replace whitespace with '+' signs
    origin = origin.replace(' ', '+')
    destination = destination.replace(' ', '+')
    url_ori = "{}address={}&key={}".format(geocode_root, origin, APP_KEY_GOECODE)
    url_des = "{}address={}&key={}".format(geocode_root, destination, APP_KEY_GOECODE)
    r_ori = requests.get(url_ori)
    r_des = requests.get(url_des)
    if r_des.status_code != 404 and r_ori.status_code != 404:
        inf_ori = r_ori.json()
        inf_des = r_des.json()
        long_ori = inf_ori["results"][0]["geometry"]["location"]["lng"]
        lati_ori = inf_ori["results"][0]["geometry"]["location"]["lat"]
        long_des = inf_des["results"][0]["geometry"]["location"]["lng"]
        lati_des = inf_des["results"][0]["geometry"]["location"]["lat"]
        url = "{}&origins={},{}&destinations={},{}&mode={}&key={}".format(distanceMatrix_root, lati_ori, long_ori,
                                                                          lati_des, long_des, transport,
                                                                          APP_KEY_DISTANCE)
        r1 = requests.get(url)
        if r1.status_code != 404:
            info = r1.json()
            ##in seconds
            duration = info["rows"][0]["elements"][0]["duration"]["value"]
            return round(duration / (60.0), 2)



def add_to_queue(person):
    # send a message to thank the user for subscribing
    # client.messages.create(to=person.phone,
    #                        body="Hi! you're been subscribed now", from_=TNUM)
    # add the number with the time they want to get messaged
    redis_server.set(person.phone, person.departure)

    ##flightTime
    # time_to_notify = datetime.fromtimestamp(person.departure, tz=pytz.UTC)
    time_to_notify = datetime.now() + timedelta(seconds=1)


    if time_to_notify != None:
        # append a phone number with the specific time
        scheduler.enqueue_at(time_to_notify, notify_number, person.phone, "please leave in an hour from now")
        scheduler.enqueue_at(time_to_notify, notify_number, person.phone, "please leave in half an hour")
        scheduler.enqueue_at(time_to_notify, call_number, person)
        print("here")
    else:
        print("something went wrong")



def notify_number(number, msg):
    client.message.create(to=number,
                          from_ = TNUM,
                          body = msg)



def call_number(person):
    client.api.account.calls.create(to=person.phone,
                                    from_ =TNUM,
                                    url = "https://ear-tube-znk.c9users.io/say/say?words={}".format("Leave now"))



# def translateAirportCode():
#
#     fileReader = csv.reader(open("Workbook2.csv"), delimiter = ",")
#     #header = fileReader.next()
#     d = {}
#     for Airports, Code, City, State in fileReader:
#         d[Code] = Airports + ', ' + City + ', ' + State
#     return d

# print(getAverageTravelTime('81 Bay State, Boston, MA', '726 Comm Ave, Boston, MA', 'walking'))
if __name__ == '__main__':
    app.run(debug=True)
