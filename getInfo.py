from flask import Flask, request
import requests
import json

app = Flask(__name__)

APP_KEY_DISTANCE = 'AIzaSyALWTLc32yxdQyw0kt3t1BwUNpcT7sp1mI'
APP_KEY_GOECODE = 'AIzaSyAWOFkVAIf0S3uUAQ6umYkwMprlQweag24'
distanceMatrix_root = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'
geocode_root = 'https://maps.googleapis.com/maps/api/geocode/json?'

users = []

@app.route('/info', methods = ['POST'])
def storeInfo():
    origin = request.form['address']
    phoneNumber = request.form['phone']
    flightNumber = request.form['flight number']
    flightTime = request.form['flight time']
    airport = request.form['destination']
    transport = request.form['transportation']
    checkin = request.form['checkin']
    person = user(phoneNumber, origin, flightNumber, flightTime, airport, transport, checkin)
    ##check no duplicates
    for i in users:
        if phoneNumber == i.phone and flightTime == i.time and flightNumber == i.flight:
            return
    users.append(person)



@app.route('/changeOri', methods = ['POST'])
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
    def __init__(self, phoneNumber, address, flightNumber, flightTime, airport, transport,  checkin):
        self.phone = phoneNumber
        self.address = address
        self.flight = flightNumber
        self.time = flightTime
        self.aiport = airport
        self.transport = transport
        self.checkin = checkin
        ##this is the most important variable
        #needs more estimations to get an accurate leaving time
        self.estimateTime = getAverageTravelTime(address, airport, transport)

    def changeDestination(self, origin):
        ##do somechanges.
        self.estimateTime = self.estimateTime - getAverageTravelTime(self.address, self.airport, self.transport) + getAverageTravelTime(origin, self.airport, self.transport)
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
        url = "{}&origins={},{}&destinations={},{}&mode={}&key={}".format(distanceMatrix_root, lati_ori, long_ori, lati_des, long_des, transport, APP_KEY_DISTANCE)
        r1 = requests.get(url)
        if r1.status_code != 404:
            info = r1.json()
            ##in seconds
            duration = info["rows"][0]["elements"][0]["duration"]["value"]
            return round(duration / (60.0),2)


print(getAverageTravelTime('81 Bay State, Boston, MA', '726 Comm Ave, Boston, MA', 'walking'))


