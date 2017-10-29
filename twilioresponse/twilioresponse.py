from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request, Response
import time
from datetime import datetime
from pytz import UTC

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def reminder(time):
    #time = time.split(':')
    now = get_time()
    if now + 3600.00 > time:
        print("Leave now!")
        return 0




def get_time():
    now = time.time()
    #print(now)
    return now


if __name__ == '__main__':

    while(True):
        dat = datetime(2017,10,29,1,18,0,0).timestamp()
        val = reminder(dat)
        if val == 0:
            break
