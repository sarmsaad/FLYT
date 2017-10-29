from redis import Redis
from rq_scheduler import Scheduler

from twilio.rest import TwilioRestClient
from datetime import datetime

#intialize the server
redis_server = Redis()

#intiliaze the scheduler
scheduler = Scheduler(connection=redis_server)

client = TwilioRestClient()

sid='ACd3d6e4fed0307c74bd8db2d07d9f4e3b'


def add_to_queue(person):
    #send a message to thank the user for subscribing
    client.messages.create(to=person.phone, messaging_service_sid = sid, body="Hi! you're been subscribed now")
    #add the number with the time they want to get messaged
    redis_server.set(person.phone,person.flightTime)

    time_to_notify = person.estimateTime

    if time_to_notify != None:
        #append a phone number with the specific time
        scheduler.enqueue_at(time_to_notify, notify_number, person, "please leave in an hour from now")
        scheduler.enqueue_at(time_to_notify, notify_number, person, "please leave in half an hour")
        scheduler.enqueue_at(time_to_notify, notify_number, person, "leave nooooow")
        print("here")
    else:
        print("something went wrong")

def notify_number(person, msg):
    #send the message 5 before leaving
    client.messages.create(to=person.phone, messaging_service_sid=sid, body=msg)





