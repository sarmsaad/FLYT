from flask import Flask, request
import requests
import json

app = Flask(__name__)

APP_KEY_DISTANCE = 'AIzaSyALWTLc32yxdQyw0kt3t1BwUNpcT7sp1mI'
APP_KEY_GOECODE = 'AIzaSyAWOFkVAIf0S3uUAQ6umYkwMprlQweag24'
distanceMatrix_root = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'
geocode_root = 'https://maps.googleapis.com/maps/api/geocode/json?'

@app.route('/info', methods = ['POST'])
def storeInfo():
    origin = request.form['address']
    phoneNumber = request.form['phone']
    flightNumber = request.form['flight number']
    flightTime = request.form['flight time']
    airport = request.form['destination']
    transport = request.form['transportation']

@app.route('/changeOri', methods = ['POST'])
def changeOrigin(origin, destination, transport):
    return getAverageTravalTime(origin, destination, transport)

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


print(getAverageTravelTime('81 Bay State, Boston, MA', '726 Comm Ave, Boston, MA', 'bicycling'))


