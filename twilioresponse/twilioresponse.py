from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request, Response
import time
from datetime import datetime
from pytz import UTC


ID = "ACd3d6e4fed0307c74bd8db2d07d9f4e3b"
token= "df0c48d047e18a0b816e5dba110dd9ed"
client = Client(ID, token)

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def reminder(phoneno, time):
    #time = time.split(':')
    now = get_time()
    if now + 3600.00 > time:
        #print("Leave now!")
        #resp = MessagingResponse()
        #resp.message("Leave now!")
        client.api.account.messages.create(
            to=phoneno,
            from_="+19712703263",
            body="Leave now!")
        print("Leave now!")
        return 0




def get_time():
    now = time.time()
    #print(now)
    return now


if __name__ == '__main__':

    while(True):
        dat = datetime(2017,10,29, 10, 14,0,0).timestamp()
        val = reminder("+18576009560",dat)
        if val == 0:
            break
