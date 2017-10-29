import requests
from redis import Redis
from rq_scheduler import Scheduler

from twilio.rest import TwilioRestClient
from datetime import datetime

#intialize the server
redis_server = Redis()
redis_server2 = Redis()

#intiliaze the scheduler
scheduler = Scheduler(connection=redis_server)
scheduler2 = Scheduler(connection=redis_server2)

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
        scheduler.enqueue_at(time_to_notify, notify_number, person.phone)
        print("here")
    else:
        print("something went wrong")

def notify_number(person):
    #send the message 5 before leaving
    client.messages.create(to=person.phone, messaging_service_sid=sid, body="please leave an hour from now")

    ##add 2 minutes so it would send a text 30 min before leaving
    flightTime = delete(person.flightTime)
    person.flightTime = flightTime
    redis_server2.set(person.phone, flightTime)

    time_to_notify = person.estimateTime #- (find a way to delete two minutes)

    if time_to_notify != None:
        scheduler2.enqueue_at(time_to_notify, notify_number2, person.phone)
        print("went here")
    else:
        print("lmao")

def notify_number2(person):
    client.messages.create(to=person.phone, messaging_service_sid=sid, body="please")




